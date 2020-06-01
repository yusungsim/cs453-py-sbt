def test_me(x):
    z = 0
    if x == 2:
        print('1')
        return report
    else:
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
