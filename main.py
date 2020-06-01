import parser as PS
import args_scanner as AS
import args_generator as AG
import ast_modifier as AM
import test_executor as TE
import ast_coverage as AC
import ast_fitness as AF
from pprint import pprint
from copy import deepcopy
import ast, astor

def main(filename):
  # some strings
  gadgetFilename = 'gadget.py'
  gadgetNames = ('g_init_report', 'g_insert_report', 'g_return_report')
  targetFunctionName = 'test_me'

  # loading test funciton AST
  tree = PS.parse_from_file(filename)
  orgtestmeDef = PS.search_fundef_name(tree, targetFunctionName)
  
  ## dummy else pass : need to insert dummy else lines
  dummyTestmeDef = deepcopy(orgtestmeDef)
  AM.change_return_fundef(dummyTestmeDef)
  AM.insert_dummy_else_fundef(dummyTestmeDef)
  dummied_source = astor.to_source(dummyTestmeDef)
  ## writing to temporary file
  dummied_filename = 'temp/' + filename
  dummied_file = open(dummied_filename, 'w')
  dummied_file.write(dummied_source)
  dummied_file.close()

  ## then reload the dummy-passed file
  tree = PS.parse_from_file(dummied_filename)
  testTree = PS.parse_from_file(dummied_filename)
  testDef = PS.search_fundef_name(testTree, targetFunctionName)
  newTestDef = deepcopy(testDef)

  # making initial test set
  testDomain = AG.get_domain(newTestDef)
  #pprint(testDomain)
  initTestSet = AG.domain_generate_input(newTestDef)
  pprint(initTestSet)

  # modifying test function AST, to make reports of traces
  AM.fundef_modifier(newTestDef, gadgetFilename, gadgetNames)
  mod_source = astor.to_source(newTestDef)
  ## also save modified source file for storage
  mod_filename = 'temp/' + filename +'.mod.py'
  mod_file = open(mod_filename, 'w')
  mod_file.write(mod_source)
  mod_file.close()

  # make branch info of origianl function (but else-dummy inserted)
  funBranchnode = TE.fundef_bnode(testDef)
  # funBranchnode.recurse_print(0)
  # pprint(TE.recursive_distance_lineno(funBranchnode, 13))

  # execute test with each arguments in init test set
  arglist = AS.get_idlist(newTestDef)
  reports = TE.generate_fundef_test_reports(newTestDef, targetFunctionName, initTestSet, arglist)
  #pprint(reports[0])
  # reports is list of report
  # report : ( args, list of trace info)
  # trace info : (lineno, dict-map`ping of var value)
  
  # make coverage information
  #for report in reports:
  #  pprint(AC.report_to_tracelines(report))
  brLineInfo = AC.bnode_to_branchlines(funBranchnode)
  #pprint(brLineInfo)
  covermap = AC.covermap_reportlist(brLineInfo, reports)
  #pprint(covermap)
  coverage = AC.coverage_from_covermap(covermap)
  print('### Coverage (total, count, percentage) ###')
  pprint(coverage)


if __name__ == '__main__':
  main('inputs/sample1.py')