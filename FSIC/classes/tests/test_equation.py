# -*- coding: utf-8 -*-


from FSIC.classes.schematic import Equation


tests = {
    'C_d = alpha_1 * YD + alpha_2 * H_h[-1]':
        {'expr': 'C_d[period] = alpha_1[period] * YD[period] + alpha_2[period] * H_h[period-1]'},
}


def test_equation():
    for string, expected in tests.items():
        output = Equation(string)
        for k, v in expected.items():
            assert output[k] == v


if __name__ == '__main__':
    import nose
    nose.runmodule()
