def test_me(x):
    report = []
    z = 0
    ln = 3
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if x == 2:
        ln = 4
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('1')
        return report
    else:
        ln = 7
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('Dummy Else')
    for i in range(x):
        print('2')
        z += 1
    else:
        print('3')
        if z == 0:
            print('4')
            return report
        while z > 0:
            print('5')
            z -= 1
    return report
    return report
