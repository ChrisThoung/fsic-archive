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


def test_identify_variables_one_exogenous_variable():
    statement = 'self.C_s[0] = self.C_d[0]'
    assert fsic.parser.code.identify_variables(statement) == (
        {'endogenous': ['self.C_s'],
         'exogenous': ['self.C_d']})


def test_identify_variables_multiple_exogenous_variables():
    statement = (
        'self.C_d[period] = '
        'self.alpha_1[period]*self.YD[period] + '
        'self.alpha_2[period]*self.H_h[period-1]')
    assert fsic.parser.code.identify_variables(statement) == (
        {'endogenous': ['self.C_d'],
         'exogenous': list(sorted(['self.alpha_1',
                                   'self.YD',
                                   'self.alpha_2',
                                   'self.H_h']))})


def test_identify_variables_one_exogenous_variable_no_prefix():
    statement = 'C_s[0] = C_d[0]'
    assert fsic.parser.code.identify_variables(statement, prefix=r'\b') == (
        {'endogenous': ['C_s'],
         'exogenous': ['C_d']})


def test_identify_variables_multiple_exogenous_variables_no_prefix():
    statement = (
        'C_d[period] = '
        'alpha_1[period] * YD[period] + '
        'alpha_2[period] * H_h[period-1]')
    assert fsic.parser.code.identify_variables(statement, prefix=r'\b') == (
        {'endogenous': ['C_d'],
         'exogenous': list(sorted(['alpha_1',
                                   'YD',
                                   'alpha_2',
                                   'H_h']))})


def test_identify_variables_multiple_lines():
    statement = '\n'.join([
        'self.C_s = self.C_d',
        'self.G_s = self.G_d',
        'self.T_s = self.T_d',
        'self.N_s = self.N_d',])
    assert fsic.parser.code.identify_variables(statement) == (
        {'endogenous': list(sorted(['self.C_s',
                                    'self.G_s',
                                    'self.T_s',
                                    'self.N_s'])),
         'exogenous': list(sorted(['self.C_d',
                                   'self.G_d',
                                   'self.T_d',
                                   'self.N_d']))})


def test_identify_variables_multiple_lines_remove_duplicates():
    statement = '\n'.join([
        'self.C_d = self.alpha_1 * self.YD + self.alpha_2 * self.H_h[-1]',
        'self.C_s = self.C_d',
        'self.G_s = self.G_d',
        'self.T_s = self.T_d',
        'self.N_s = self.N_d',
        'self.T_d = self.theta * self.W * self.N_d'])
    assert fsic.parser.code.identify_variables(statement) == (
        {'endogenous': list(sorted(['self.C_d',
                                    'self.C_s',
                                    'self.G_s',
                                    'self.T_s',
                                    'self.N_s',
                                    'self.T_d', ])),
         'exogenous': list(sorted(['self.alpha_1',
                                   'self.YD',
                                   'self.alpha_2',
                                   'self.H_h',
                                   'self.G_d',
                                   'self.N_d',
                                   'self.theta',
                                   'self.W', ]))})


def test_identify_variables_multiple_lines_keep_duplicates():
    statement = '\n'.join([
        'self.C_d = self.alpha_1 * self.YD + self.alpha_2 * self.H_h[-1]',
        'self.C_s = self.C_d',
        'self.G_s = self.G_d',
        'self.T_s = self.T_d',
        'self.N_s = self.N_d',
        'self.T_d = self.theta * self.W * self.N_d'])
    assert fsic.parser.code.identify_variables(
        statement,
        remove_duplicates=False) == (
        {'endogenous': list(sorted(['self.C_d',
                                    'self.C_s',
                                    'self.G_s',
                                    'self.T_s',
                                    'self.N_s',
                                    'self.T_d', ])),
         'exogenous': list(sorted(['self.alpha_1',
                                   'self.YD',
                                   'self.alpha_2',
                                   'self.H_h',
                                   'self.C_d',
                                   'self.G_d',
                                   'self.T_d',
                                   'self.N_d',
                                   'self.theta',
                                   'self.W',
                                   'self.N_d']))})


if __name__ == '__main__':
    import nose
    nose.runmodule()
