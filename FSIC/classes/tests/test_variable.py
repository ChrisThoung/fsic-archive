# -*- coding: utf-8 -*-


from FSIC.classes.schematic import Variable


tests = {
    'C_d': {'name': 'C_d', 'index': 0, 'index_string': '', 'expr': 'C_d[period]'},
    'H_s[-1]': {'name': 'H_s', 'index': -1, 'index_string': '-1', 'expr': 'H_s[period-1]'},
    'Y[0]': {'name': 'Y', 'index': 0, 'index_string': '', 'expr': 'Y[period]'},
    'Y[1]': {'name': 'Y', 'index': 1, 'index_string': '+1', 'expr': 'Y[period+1]'},
}


def test_variable():
    for string, expected in tests.items():
        output = Variable(string)
        for k, v in expected.items():
            assert output[k] == v


if __name__ == '__main__':
    import nose
    nose.runmodule()
