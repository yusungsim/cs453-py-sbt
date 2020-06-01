import ast, astor
import test_executor as TE
import args_generator as AG
import ast_modifier as AM

# calculates coverage
# branchlines : list of line number of each if body and else body
# traceliens : list of line nubmer of executed lines
# covermap : mapping(dict), linenumber -> True/False (covered or not)
def covermap(branchlines, tracelines):
  cover = dict()
  for br in branchlines:
    cover[br] = False
  for tr in tracelines:
    cover[tr] = True
  return cover

def coverage_from_covermap(cmap):
  assert(isinstance(cmap, dict))
  total = len(cmap.keys())
  count = 0
  for ln, covered in cmap.items():
    if covered:
      count += 1
  return (total, count, count/total * 100)

# reports to tracelines
def report_to_tracelines(report):
  traces = report[1]
  assert(isinstance(traces, list))
  # only collect covered lines
  tracelines = []
  for ln, mapping in traces:
    tracelines.append(ln)
  return tracelines

# list of reports to covermap
def covermap_reportlist(branchlines, reportlist):
  cover = covermap(branchlines, [])
  for report in reportlist:
    tlines = report_to_tracelines(report)
    for ln in tlines:
      cover[ln] = True
  return cover

# bnode to branchlines
def bnode_to_branchlines(bnode):
  assert(isinstance(bnode, TE.BranchNode))
  result = []
  if bnode.left != None and bnode.right != None:
    lres = bnode_to_branchlines(bnode.left)
    rres = bnode_to_branchlines(bnode.right)
    result.append(bnode.lineno)
    result = result + lres + rres
  if bnode.next != None:
    result = result + bnode_to_branchlines(bnode.next)
  return sorted(result)

