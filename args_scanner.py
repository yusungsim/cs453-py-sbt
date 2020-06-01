import ast, astor
import parser as PS
from pprint import pprint

def arg_to_id(arg):
  return arg.arg

def get_arglist(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  return fundef.args.args

def get_idlist(fundef):
  assert(isinstance(fundef, ast.FunctionDef))
  arglist = get_arglist(fundef)
  idlist = list(map(arg_to_id, arglist))
  return idlist

### test section
def main():
  filename = 'inputs/sample1.py'
  tree = PS.parse_from_file(filename)
  testmeDef = PS.search_fundef_name(tree, 'test_me')
  idlist = get_idlist(testmeDef)
  pprint(idlist)

if __name__ == '__main__':
  main()