import test_executor as TE
import ast_coverage as AC
from math import inf as INF
from pprint import pprint

def dist_bnode_ln(bnode, ln):
  assert(isinstance(bnode, TE.BranchNode))
  if bnode.lineno == ln:
    return 0
  dist = INF
  if bnode.left != None and bnode.right != None:
    ldist = dist_bnode_ln(bnode.left, ln) + 1
    rdist = dist_bnode_ln(bnode.right, ln) + 1
    dist = min(ldist, rdist, dist)
  if bnode.next != None:
    ndist = dist_bnode_ln(bnode.next, ln)
    dist = min(ndist, dist)
  return dist

def find_bnode_with_ln(bnode, ln):
  assert(isinstance(bnode, TE.BranchNode))
  if bnode.lineno == ln:
    return bnode
  res = None
  if bnode.left != None:
    lres = find_bnode_with_ln(bnode.left, ln)
    if lres != None:
      res = lres
  if bnode.right != None:
    rres = find_bnode_with_ln(bnode.right, ln)
    if rres != None:
      res = rres
  if bnode.next != None:
    nres = find_bnode_with_ln(bnode.next, ln)
    if nres != None:
      res = nres
  return res

def bnode_ln_distance(bnode, fromln, toln):
  startNode = find_bnode_with_ln(bnode, fromln)
  if startNode == None:
    return INF
  dist = dist_bnode_ln(startNode, toln)
  return dist

def tracelines_ln_distance(bnode, tracelines, targetln):
  dist = INF
  for fromln in tracelines:
    cur = bnode_ln_distance(bnode, fromln, targetln)
    dist = min(dist, cur)
  return dist

def report_ln_distance(bnode, report, targetln):
  tracelines = AC.report_to_tracelines(report)
  return tracelines_ln_distance(bnode, tracelines, targetln)

def find_tf_linenums(bnode, brln):
  if bnode == None:
    return None
  if bnode.lineno == brln:
    return (bnode.left.lineno, bnode.right.lineno)
  result = None
  if bnode.left != None:
    lres = find_tf_linenums(bnode.left, brln)
    if lres != None:
      result = lres
  if bnode.right != None:
    rres = find_tf_linenums(bnode.right, brln)
    if rres != None:
      result = rres
  if bnode.next != None:
    nres = find_tf_linenums(bnode.next, brln)
    if nres != None:
      result = nres
  return result