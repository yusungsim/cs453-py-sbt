def test_me(x, y, z):
    report = []
    ln = 2
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if y > 13:
        ln = 3
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('1')
        ln = 4
        br = 'br'
        case = ln, br, deepcopy(locals())
        report.append(case)
        if x < 2:
            ln = 5
            br = 'if'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('2')
            z = 3
            ln = 7
            br = 'br'
            case = ln, br, deepcopy(locals())
            report.append(case)
            if x < -1:
                ln = 8
                br = 'if'
                case = ln, br, deepcopy(locals())
                report.append(case)
                print('3')
                z = 1
            else:
                ln = 11
                br = 'else'
                case = ln, br, deepcopy(locals())
                report.append(case)
                print('Dummy Else')
        else:
            ln = 13
            br = 'else'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('Dummy Else')
    else:
        ln = 15
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('4')
        x = 2
    y = 50
    ln = 18
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if z == 4:
        ln = 19
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('5')
        z = 1
    else:
        ln = 22
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('6')
        while x < 5:
            print('7')
            x += 1
            z = z + 1
    y = 0
    return report
