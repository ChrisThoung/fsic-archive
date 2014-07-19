# -*- coding: utf-8 -*-


import fsic.parser.code


def test_one_line_no_lags():
    block = 'Y = W * N_d'
    assert fsic.parser.code.translate(block) == (
        'self.Y[period] = self.W[period] * self.N_d[period]')


def test_one_line_no_lags_custom_period():
    block = 'T_s = T_d'
    assert fsic.parser.code.translate(block, period='time') == (
        'self.T_s[time] = self.T_d[time]')


if __name__ == '__main__':
    import nose
    nose.runmodule()
