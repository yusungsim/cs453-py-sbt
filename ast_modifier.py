import ast, astor
import parser as PS
from copy import deepcopy
from pprint import pprint

# Note
# 1) Current implementation directly modifies AST object. Should it changed into pure functions? It will require deepcopy
# 2) Design of modifying functions
# def function(x, y, z):
#   report = []
#   <original code>
#   if ???:
#     report.append((<linenumber>, locals))
#   else ???:
#     report.append((<linenumber>, locals))

### AST modifier
# inserts given statment into body, in given index
def insert_stmt_at(body, stmt, index):
  assert(isinstance(body, list))
  assert(0 <= index and index <= len(body))
  body.insert(index, stmt)

# inserts given body into body, in given index
def insert_body_at(dst_body, src_body, index):
  assert(isinstance(dst_body, list))
  assert(isinstance(src_body, list))
  assert(0 <= index and index <= len(dst_body))
  for stmt in src_body:
    dst_body.insert(index, stmt)
    index += 1

### some utility function to load gadgets
def search_gadget(gadgetFileName, gadgetName):
  tree = PS.parse_from_file(gadgetFileName)
  gFunDef = PS.search_fundef_name(tree, gadgetName)
  return gFunDef

def make_insert_gadget(gFunDef, lineno, branch):
  assert(isinstance(gFunDef, ast.FunctionDef))
  ln_source = 'ln = ' + str(lineno)
  br_source = 'br = ' + str(branch)
  expr = ast.parse(ln_source).body[0]
  expr2 = ast.parse(br_source).body[0]
  newFunDef = deepcopy(gFunDef)
  insert_stmt_at(newFunDef.body, expr, 0)
  insert_stmt_at(newFunDef.body, expr2, 1)
  return newFunDef

### have to insert some dummy line for else branch
def insert_dummy_else(body):
  for stmt in body:
    if isinstance(stmt, ast.If):
      # blank else case
      if len(stmt.orelse) == 0:
        dummy = ast.parse('print("Dummy Else")').body[0]
        insert_stmt_at(stmt.orelse, dummy, 0)
      insert_dummy_else(stmt.body)
      insert_dummy_else(stmt.orelse)
  
def insert_dummy_else_fundef(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  insert_dummy_else(fundef.body)

### have to change all return statement into 'return report
ret_source = 'return report'
ret_tree = ast.parse(ret_source)
ret_val = ret_tree.body[0].value

def change_return_report(body):
  assert(isinstance(body, list))
  for stmt in body:
    if isinstance(stmt, ast.If):
      change_return_report(stmt.body)
      change_return_report(stmt.orelse)
    elif isinstance(stmt, ast.Return):
      stmt.value = ret_val
    elif isinstance(stmt, ast.For):
      change_return_report(stmt.body)
      change_return_report(stmt.orelse)
    elif isinstance(stmt, ast.While):
      change_return_report(stmt.body)
      change_return_report(stmt.orelse)

def change_return_fundef(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  change_return_report(fundef.body)

### test function AST modifier
def insert_gadget_recursive(body, gFunDef):
  assert(isinstance(body, list))
  assert(isinstance(gFunDef, ast.FunctionDef))
  # base case: no need to insert for empty list
  if len(body) == 0:
    return
  insertQ = []
  # recursive case : iterate over body's statements
  for stmt in body:
    # If case : recursively inssert to if body and else body
    if isinstance(stmt, ast.If):
      # first insert "br" gadget
      ln = stmt.body[0].lineno - 1
      brGadget = make_insert_gadget(gFunDef, ln, '"br"')
      insertQ.append((body.index(stmt), brGadget))
      # then make ifbody, elsebody gadget
      ifln = stmt.body[0].lineno
      elseln = stmt.orelse[0].lineno # dummy else is inserted so safe to access this
      # make gadget to insert 
      ifGadget = make_insert_gadget(gFunDef, ifln, '"if"')
      elseGadget = make_insert_gadget(gFunDef, elseln, '"else"')
      # insert each gadget to ifbody and elsebody
      insert_body_at(stmt.body, ifGadget.body, 0)
      insert_body_at(stmt.orelse, elseGadget.body, 0)
      # recursive call
      insert_gadget_recursive(stmt.body, gFunDef)
      insert_gadget_recursive(stmt.orelse, gFunDef)
  # finally insert "br"gadgets in insertQ
  delta = 0
  for index, gadget in insertQ:
    insert_body_at(body, gadget.body, index + delta)
    delta += len(gadget.body)

def test_fundef_modifier(testFunDef, gInitDef, gInsDef, gRetDef):
  assert(isinstance(testFunDef, ast.FunctionDef))
  assert(isinstance(gInitDef, ast.FunctionDef))
  assert(isinstance(gInsDef, ast.FunctionDef))
  assert(isinstance(gRetDef, ast.FunctionDef))
  # non-pure function: diretly modifies the fundef object given as args
  testBody = testFunDef.body
  insert_gadget_recursive(testBody, gInsDef)
  insert_body_at(testBody, gInitDef.body, 0)
  insert_body_at(testBody, gRetDef.body, len(testBody))
  
def fundef_exec_wrapper(fundef, fname, args):
  assert(isinstance(fundef, ast.FunctionDef))
  assert(isinstance(fname, str))
  localEnv = {}
  globEnv = {'deepcopy': deepcopy}
  source = astor.to_source(fundef)
  exec(source, globEnv, localEnv)
  funobj = localEnv[fname]
  result = funobj(*args)
  return result
  
# total wrapper for modifying fundef with gadgets
# caveat: this function is modifier: argument fundef object will be changed
def fundef_modifier(fundef, gFileName, gadgetnames):
  assert(isinstance(fundef, ast.FunctionDef))
  assert(len(gadgetnames) == 3)
  initGadget = search_gadget(gFileName, gadgetnames[0])
  insertGadget = search_gadget(gFileName, gadgetnames[1])
  returnGadget = search_gadget(gFileName, gadgetnames[2])
  test_fundef_modifier(fundef, initGadget, insertGadget, returnGadget)

def main():
  testFileName = 'inputs/sample1.py'
  testFunName = 'test_me'
  testmeDef = PS.search_fundef_name(PS.parse_from_file(testFileName), testFunName)
  gFileName = 'gadget.py'
  initGadget = search_gadget(gFileName, 'g_init_report')
  insertGadget = search_gadget(gFileName, 'g_insert_report')
  returnGadget = search_gadget(gFileName, 'g_return_report')
  #newInsGadget = make_insert_gadget(insertGadget, 42)
  #pprint(newInsGadget.__dict__)
  #insert_gadget_recursive(testmeDef.body, insertGadget)
  #newsource = astor.to_source(testmeDef)
  #pprint(newsource)
  ### Need 2 pass : first, insert dummy else, and inserting gadgets
  insert_dummy_else_fundef(testmeDef)
  test_fundef_modifier(testmeDef, initGadget, insertGadget, returnGadget)
  pprint(astor.to_source(testmeDef))
  #result = fundef_exec_wrapper(testmeDef, testFunName, [1,2,3])
  #pprint(result)
  

if __name__ == '__main__':
  main()