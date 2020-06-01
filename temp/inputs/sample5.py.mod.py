def test_me(a, b, c):
    report = []
    d = 0
    ln = 3
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if a > b + c:
        ln = 4
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('1')
        ln = 5
        br = 'br'
        case = ln, br, deepcopy(locals())
        report.append(case)
        if b != c:
            ln = 6
            br = 'if'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('2')
            d += 1
        else:
            ln = 9
            br = 'else'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('3')
            d += 2
    else:
        ln = 12
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('4')
        d = d - 1
    ln = 14
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if d > 0:
        ln = 15
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('5')
        ln = 16
        br = 'br'
        case = ln, br, deepcopy(locals())
        report.append(case)
        if a > 0:
            ln = 17
            br = 'if'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('6')
            return report
        else:
            ln = 20
            br = 'else'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('7')
            return report
    else:
        ln = 23
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('8')
        return report
    return report
