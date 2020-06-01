import ast
import ast_modifier as AM
import parser as PS
from math import inf as INF
from pprint import pprint

def generate_fundef_test_reports(fundef, funname, testset, targetvar):
  assert(isinstance(fundef, ast.FunctionDef))
  assert(isinstance(testset, list))
  assert(isinstance(targetvar, list))
  reports = []
  for args in testset:
    # trace is list of tuple of (linenum, dictionary),
    # where dictionary is mapping of variable_id -> value
    traces = AM.fundef_exec_wrapper(fundef, funname, args)
    #pprint(traces)
    # generate a report for specific arguments
    arg_report = []
    for t in traces:
      lineno = t[0]
      br = t[1]
      varMap = t[2]
      targetVarMap = dict()
      for name in targetvar:
        value = varMap[name]
        targetVarMap[name] = value
      t_report = (lineno, targetVarMap)
      arg_report.append(t_report)
    # append the report
    reports.append((args, arg_report))
  return reports

# tree-structure that only saves branch line number info
class BranchNode():
  def __init__(self, ln, l, r, n):
    self.lineno = ln
    self.left = l
    self.right = r
    self.next = n
  def recurse_print(self, depth):
    print('\t' * depth, 'line: ', self.lineno)
    if self.left != None:
      self.left.recurse_print(depth + 1)
    if self.right != None:
      self.right.recurse_print(depth + 1)
    if self.next != None:
      self.next.recurse_print(depth)

def recursive_bnode_body(body):
  assert(isinstance(body, list))
  if len(body) == 0:
    return None
  stmt = body[0]
  current_ln = stmt.lineno
  bnode = None
  nextNode = None
  if len(body) >= 2:
    nextNode = recursive_bnode_body(body[1:])
  # if case
  if isinstance(stmt, ast.If):
    ifBody = stmt.body
    elseBody = stmt.orelse
    ifNode = recursive_bnode_body(ifBody)
    elseNode = recursive_bnode_body(elseBody)
    bnode = BranchNode(current_ln, ifNode, elseNode, nextNode)
  # other cases 
  else:
    bnode = BranchNode(current_ln, None, None, nextNode)
  return bnode

def fundef_bnode(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  return recursive_bnode_body(fundef.body)

def recursive_distance_lineno(bnode, ln):
  currentln = bnode.lineno
  if currentln == ln:
    return 0
  else:
    ldist = -1
    rdist = -1
    ndist = -1
    # recursively get distance of left/right/next node to ln
    if bnode.left != None:
      ldist = recursive_distance_lineno(bnode.left, ln)
    if bnode.right != None:
      rdist = recursive_distance_lineno(bnode.right, ln)
    if bnode.next != None:
      ndist = recursive_distance_lineno(bnode.next, ln)
    # if distance not found: no path, so return -1
    if ldist == -1 and rdist == -1 and ndist == -1:
      return -1
    # if distance found: select minimu distance
    else:
      dist = INF
      if ldist != -1:
        dist = min(dist, ldist + 1)
      if rdist != -1 :
        dist = min(dist, rdist + 1)
      if ndist != -1:
        dist = min(dist, ndist)
      return dist

def main():
  filename = 'inputs/sample1.py'
  testname = 'test_me'
  tree = PS.parse_from_file(filename)
  fundef = PS.search_fundef_name(tree, testname)
  funBranchNode = fundef_bnode(fundef)
  funBranchNode.recurse_print(0)
  pprint(recursive_distance_lineno(funBranchNode, 14))
  

if __name__ == '__main__':
  main()
