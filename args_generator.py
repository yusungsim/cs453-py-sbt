import ast, astor
from math import inf as INF
import args_scanner as AS
import parser as PS
from pprint import pprint
import random

# Note
# 1) will get ast.Compare object and input domain, and divide the domain
# 2) 'domain' : mapping(dictionary) variable_id -> (min, max)

# scanning all ast.Compare object
def extract_compare_if(ifstmt):
  assert(isinstance(ifstmt, ast.If))
  test = ifstmt.test
  lexp = test.left
  # assume only one comparator and right expr
  rexp = test.comparators[0]
  cop = test.ops[0]
  return (lexp, rexp, cop)

# paring comp tuple into easy-using form
def translate_compare_tup(comp):
  lexp = comp[0]
  rexp = comp[1]  
  cop = comp[2]
  l = None
  r = None
  o = None
  # parse left and right by class type
  # LHS : variable, constant (positive and negative)
  # other cases cannot be handled, so becomes None
  if isinstance(lexp, ast.Name):
    l = lexp.id
  elif isinstance(lexp, ast.Constant):
    l = lexp.value
  elif isinstance(lexp, ast.UnaryOp):
    if isinstance(lexp.op, ast.USub):
      v = lexp.operand.value
      r = - v
  # RHS : variable, constant (positive and negative)
  if isinstance(rexp, ast.Name):
    r = rexp.id
  elif isinstance(rexp, ast.Constant):
    r = rexp.value
  elif isinstance(rexp, ast.UnaryOp):
    if isinstance(rexp.op, ast.USub):
      v = rexp.operand.value
      r = - v
  # parse operator into single string obj
  # total 5 cases : >, <, ==, >=, <=
  if isinstance(cop, ast.Gt):
    o = '>'
  elif isinstance(cop, ast.Lt):
    o = '<'
  elif isinstance(cop, ast.Eq):
    o = '=='
  elif isinstance(cop, ast.GtE):
    o = '>='
  elif isinstance(cop, ast.LtE):
    o = '<='
  return (l, o, r)
  
# if stmt -> test tupline in one pass
def extract_test_tuple(ifstmt):
  assert(isinstance(ifstmt, ast.If))
  comp = extract_compare_if(ifstmt)
  tt = translate_compare_tup(comp)
  return tt

# extract recursively from fundef
def extract_tests_body(body):
  assert(isinstance(body, list))
  tests = []
  for stmt in body:
    if isinstance(stmt, ast.If):
      tt = extract_test_tuple(stmt)
      tests.append(tt)
      if_tests = extract_tests_body(stmt.body)
      else_tests = extract_tests_body(stmt.orelse)
      tests = tests + if_tests
      tests = tests + else_tests
  return tests

def extract_tests_fundef(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  return extract_tests_body(fundef.body)

### domain maker
def initial_domain_list(arglist):
  dom = dict()
  for id in arglist:
    dom[id] = (-INF, INF)
  return [dom]

# Domain divider : gets a input domain, and a test
# then returns list of another input domain
def div_domain_by_test(dom, test):
  assert(isinstance(dom, dict))
  lhs = test[0]
  op = test[1]
  rhs = test[2]
  targetId = None
  targetNum = None
  # if non-handled case (lhs or rhs is None)
  if lhs == None or rhs == None:
    return [dom]
  # first, get targetId and targetNum
  if isinstance(lhs, str):
    targetId = lhs
  if isinstance(rhs, str):
    targetId = rhs
  if isinstance(lhs, int):
    targetNum = lhs
  if isinstance(rhs, int):
    targetNum = rhs
  # if some target is None, just return
  if targetId == None or targetNum == None:
    return [dom]
  # if targetId and targetNum set, try find targetId from dom
  if targetId not in dom.keys():
    return [dom]
  # if targetId in domain, get the min and max
  targetMin, targetMax = dom[targetId]
  # case-by-case on op
  if op in ['>=', '<=', '<', '>']:
    if targetMin < targetNum and targetNum < targetMax:
      lRange = (targetMin, targetNum)
      rRange = (targetNum, targetMax)
      newdom1 = dict(dom)
      newdom2 = dict(dom)
      newdom1[targetId] = lRange
      newdom2[targetId] = rRange
      return [newdom1, newdom2]
    else:
      return [dom]
  elif op in ['==']:
    if targetMin < targetNum and targetNum < targetMax:
      lRange = (targetMin, targetNum)
      mRange = (targetNum, targetNum)
      rRange = (targetNum, targetMax)
      newdom1 = dict(dom)
      newdom2 = dict(dom)
      newdom3 = dict(dom)
      newdom1[targetId] = lRange
      newdom2[targetId] = mRange
      newdom3[targetId] = rRange
      return [newdom1, newdom2, newdom3]
    elif targetMin == targetNum:
      lRange = (targetMin, targetNum)
      rRange = (targetNum, targetMax)
      newdom1 = dict(dom)
      newdom2 = dict(dom)
      newdom1[targetId] = lRange
      newdom2[targetId] = rRange
      return [newdom1, newdom2]
    elif targetMax == targetNum:
      lRange = (targetMin, targetNum)
      rRange = (targetNum, targetMax)
      newdom1 = dict(dom)
      newdom2 = dict(dom)
      newdom1[targetId] = lRange
      newdom2[targetId] = rRange
      return [newdom1, newdom2]
    else:
      return [dom]
  
# list of domain wrapper
def div_domain_all(domlist, testlist):
  result = []
  for d in domlist:
    result.append(d)
  for t in testlist:
    temp = []
    for d in result:
      newdom = div_domain_by_test(d, t)
      temp = temp + newdom
    result = temp
  return result

# given dom list, make a concretization
def concretize_dom_list(domlist):
  INT_MIN = - (2**10)
  INT_MAX = 2**10 - 1
  DELTA = 2**8
  assert(isinstance(domlist, list))
  arglist = []
  for dom in domlist:
    arg = []
    for name, rn in dom.items():
      Min, Max = rn
      if Min == -INF:
        if Max != INF:
          Min = Max - DELTA
        else:
          Min = INT_MIN
      if Max == INF:
        if Min != -INF:
          Max = Min + DELTA
        else:
          Max = INT_MAX
      # pick a random int inside the range
      num = random.randint(Min, Max)
      arg.append(num)
    argtup = tuple(arg)
    arglist.append(argtup)
  return arglist

# wrapper for generating the concretized inputs
def domain_generate_input(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  testlist = extract_tests_fundef(fundef)
  arglist = AS.get_idlist(fundef)
  domain_list = initial_domain_list(arglist)
  new_domain_list = div_domain_all(domain_list, testlist)
  concretized = concretize_dom_list(new_domain_list)
  return concretized

def get_domain(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  testlist = extract_tests_fundef(fundef)
  arglist = AS.get_idlist(fundef)
  domain_list = initial_domain_list(arglist)
  new_domain_list = div_domain_all(domain_list, testlist)
  return new_domain_list

# test section
def main():
  # get fundef from source
  filename = 'inputs/sample1.py'
  tree = PS.parse_from_file(filename)
  testmeDef = PS.search_fundef_name(tree, 'test_me')
  # get all if-test list
  testlist = extract_tests_fundef(testmeDef)
  # get arglist of fundef
  arglist = AS.get_idlist(testmeDef)
  # make default domain list
  domain_list = initial_domain_list(arglist)
  
  new_domain_list = div_domain_all(domain_list, testlist)
  pprint("Init domain")
  pprint(domain_list)
  pprint("Tests")
  pprint(testlist)
  pprint("newly gen domains")
  pprint(new_domain_list)

  concretized = concretize_dom_list(new_domain_list)
  pprint(concretized)

  #t1 = testlist[3]
  #d1 = domain_list[0]
  #pprint(t1)
  #pprint(d1)
  #pprint(div_domain_by_test(d1, t1))


if __name__ == '__main__':
  main()