import ast, astor

# Note on Python AST object class
# 1) statement is one AST object, with AST class (ex. ast.If, ast.Assign)
# 2) Function body, if body, else body, etc... is list of AST object

### Basic AST loader
# parse_from_file : return AST object of given python source file
# The object represents Module object on the top
def parse_from_file(filename):
  tree = astor.code_to_ast.parse_file(filename)
  return tree

# search_fundef_name: return FunctionDef AST object from Module AST
# by given function name.
def search_fundef_name(tree, name):
  assert(isinstance(tree, ast.Module))
  for fundef in tree.body:
    if isinstance(fundef, ast.FunctionDef):
      if fundef.name == name:
        return fundef
  return None 