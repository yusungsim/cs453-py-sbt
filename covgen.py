import parser as PS
import args_scanner as AS
import args_generator as AG
import ast_modifier as AM
import test_executor as TE
import ast_coverage as AC
import ast_fitness as AF
from copy import deepcopy
import ast, astor
import sys

report = ""

def test_file(filename):
  def report_print(s):
    print(s)
    global report
    report = report + s + '\n'

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

  # modifying test function AST, to make reports of traces
  AM.fundef_modifier(newTestDef, gadgetFilename, gadgetNames)
  mod_source = astor.to_source(newTestDef)
  ## also save modified source file for storage
  mod_filename = 'temp/' + filename +'.mod.py'
  mod_file = open(mod_filename, 'w')
  mod_file.write(mod_source)
  mod_file.close()

  # making initial test set
  testDomain = AG.get_domain(newTestDef)
  initTestSet = AG.domain_generate_input(newTestDef)

  # make branch info of origianl function (but else-dummy inserted)
  funBranchnode = TE.fundef_bnode(testDef)

  # execute test with each arguments in init test set
  brLineInfo = AC.bnode_to_branchlines(funBranchnode)
  arglist = AS.get_idlist(newTestDef)
  reports = TE.generate_fundef_test_reports(newTestDef, targetFunctionName, initTestSet, arglist)

  # output section : coverage info
  report_print('### Test generation for filename: ' + filename + ' ###')
  report_print("")
  report_print('1) Target funtion: ' + targetFunctionName + ', args: ' + str(arglist))
  report_print("")
  report_print('2) Generated Test inputs')
  for dom, args in zip(testDomain, initTestSet):
    report_print('Abs Domain: ' + str(dom) + ', --> Concretized input: ' + str(args))

  report_print("")
  report_print('3) Branch coverage information')
  report_print('Format: <branch line number> <T/F>: <input that covers the branch>')
  report_print('None is printed when uncovered')
  for bln in brLineInfo:
    (trueinfo, falseinfo) = search_corres_cover(funBranchnode, reports, bln)
    report_print(str(bln) + "T : " + str(trueinfo))
    report_print(str(bln) + "F : " + str(falseinfo))

  report_filename = 'outputs/' + filename + '.txt'
  report_print("")
  report_print('Test report also saved at ' + report_filename)
  report_file = open(report_filename, 'w')
  report_file.write(report)
  report_file.close()


### util function
def search_corres_cover(bnode, reports, branchln):
  truearg = None
  falsearg = None
  for report in reports:
    args = report[0]
    tracelines = AC.report_to_tracelines(report)
    trueLn, falseLn = AF.find_tf_linenums(bnode, branchln)
    if truearg == None and trueLn in tracelines:
      truearg = args
    if falsearg == None and falseLn in tracelines:
      falsearg = args
  return (truearg, falsearg)

if __name__ == '__main__':
  argv = sys.argv
  argc = len(argv)
  if argc <= 1:
    print('Please provide test target .py file as commandline argument.')
  else:
    filename = argv[1]
    test_file(filename)