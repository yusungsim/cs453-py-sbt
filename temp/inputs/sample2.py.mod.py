def test_me(x, y, z):
    report = []
    ln = 2
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if y == 100003:
        ln = 3
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('1')
        z = 1
    else:
        ln = 6
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('2')
        x = 2
    return report
