# files for gadgets, which inserted to target function
def g_init_report():
  report = []

# infront of this function body, `ln = <linenumber>` will be inserted
# and also 'br = "if"' or 'br = "else"'.
def g_insert_report():
  case = (ln, br, deepcopy(locals()))
  report.append(case)

def g_return_report():
  return report