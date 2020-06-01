def test_me(x, y, z):
    report = []
    a = 0
    b = 0
    c = 0
    ln = 5
    br = 'br'
    case = ln, br, deepcopy(locals())
    report.append(case)
    if x == 4:
        ln = 6
        br = 'if'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('1')
        a += 1
        ln = 8
        br = 'br'
        case = ln, br, deepcopy(locals())
        report.append(case)
        if x + y == 100:
            ln = 9
            br = 'if'
            case = ln, br, deepcopy(locals())
            report.append(case)
            print('2')
            a += 1
            ln = 11
            br = 'br'
            case = ln, br, deepcopy(locals())
            report.append(case)
            if z > 112831829389:
                ln = 12
                br = 'if'
                case = ln, br, deepcopy(locals())
                report.append(case)
                print('3')
                a += 1
            else:
                ln = 15
                br = 'else'
                case = ln, br, deepcopy(locals())
                report.append(case)
                print('4')
        else:
            ln = 16
            br = 'else'
            case = ln, br, deepcopy(locals())
            report.append(case)
            ln = 16
            br = 'br'
            case = ln, br, deepcopy(locals())
            report.append(case)
            if x + y == 40:
                ln = 17
                br = 'if'
                case = ln, br, deepcopy(locals())
                report.append(case)
                print('5')
            else:
                ln = 19
                br = 'else'
                case = ln, br, deepcopy(locals())
                report.append(case)
                print('Dummy Else')
    else:
        ln = 21
        br = 'else'
        case = ln, br, deepcopy(locals())
        report.append(case)
        print('Dummy Else')
    return report
