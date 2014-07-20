# -*- coding: utf-8 -*-


import fsic.parser.code


def test_one_line_no_lag():
    block = 'Y = W * N_d'
    assert fsic.parser.code.translate(block) == (
        'self.Y[period] = self.W[period] * self.N_d[period]')


def test_one_line_no_lag_custom_period():
    block = 'T_s = T_d'
    assert fsic.parser.code.translate(block, period='time') == (
        'self.T_s[time] = self.T_d[time]')


def test_one_line_lag():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[-1]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lead():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[+1]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period+1]')


def test_one_line_lead_no_sign():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[1]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period+1]')


def test_one_line_lag_single_space():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h [-1]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lag_multiple_spaces():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h  [-1]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lag_inner_space():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[ -1 ]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lag_no_spaces():
    block = 'C_d=alpha_1*YD+alpha_2*H_h[-1]'
    assert fsic.parser.code.translate(block) == (
        'self.C_d[period]='
        'self.alpha_1[period]*self.YD[period]+'
        'self.alpha_2[period]*self.H_h[period-1]')


if __name__ == '__main__':
    import nose
    nose.runmodule()
