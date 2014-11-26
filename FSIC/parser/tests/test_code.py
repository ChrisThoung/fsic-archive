# -*- coding: utf-8 -*-
"""
test_code
=========
Example equations are from, or based on, those from:

* Model SIM, from Chapter 3 of Godley and Lavoie (2007)
* Model PCEX, from Chapter 4 of Godley and Lavoie (2007)
* The AMI model, from Chapter 1 of Almon (2014)

"""


import re
import FSIC.parser.code


def test_one_line_no_lag():
    block = 'Y = W * N_d'
    assert FSIC.parser.code.translate(block) == (
        'self.Y[period] = self.W[period] * self.N_d[period]')


def test_one_line_hardcoded_parameter():
    block = 'T_d = 0.2 * W * N_s'
    assert FSIC.parser.code.translate(block) == (
        'self.T_d[period] = 0.2 * self.W[period] * self.N_s[period]')


def test_one_line_with_function():
    block = 'PQ = max(Q, PQ[-1])'
    assert FSIC.parser.code.translate(block) == (
        'self.PQ[period] = max(self.Q[period], self.PQ[period-1])')


def test_one_line_no_lag_custom_period():
    block = 'T_s = T_d'
    assert FSIC.parser.code.translate(block, period='time') == (
        'self.T_s[time] = self.T_d[time]')


def test_one_line_lag():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[-1]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lead():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[+1]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period+1]')


def test_one_line_lead_no_sign():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[1]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period+1]')


def test_one_line_lag_single_space():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h [-1]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lag_multiple_spaces():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h  [-1]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lag_inner_space():
    block = 'C_d = alpha_1 * YD + alpha_2 * H_h[ -1 ]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')


def test_one_line_lag_no_spaces():
    block = 'C_d=alpha_1*YD+alpha_2*H_h[-1]'
    assert FSIC.parser.code.translate(block) == (
        'self.C_d[period]='
        'self.alpha_1[period]*self.YD[period]+'
        'self.alpha_2[period]*self.H_h[period-1]')


def test_translate_with_import_statement():
    block = '''\
import math
C_d = alpha_1 * math.log(YD) + alpha_2 * math.log(H_h[-1])
C_d = math.exp(C_d)'''
    expected = '''\
import math
self.C_d[period] = self.alpha_1[period] * math.log(self.YD[period]) + \
self.alpha_2[period] * math.log(self.H_h[period-1])
self.C_d[period] = math.exp(self.C_d[period])'''
    result = FSIC.parser.code.translate(block)
    assert result == expected


def test_translate_with_from_import_statement():
    block = '''\
from random import normalvariate
Ra = normalvariate(0, 1)
YD_e = YD * (1 + Ra)'''
    expected = '''\
from random import normalvariate
self.Ra[period] = normalvariate(0, 1)
self.YD_e[period] = self.YD[period] * (1 + self.Ra[period])'''
    result = FSIC.parser.code.translate(block)
    assert result == expected


def test_identify_variables_one_exogenous_variable():
    statement = 'self.C_s[0] = self.C_d[0]'
    assert FSIC.parser.code.identify_variables(statement) == (
        {'endogenous': ['self.C_s'],
         'exogenous': ['self.C_d']})


def test_identify_variables_multiple_exogenous_variables():
    statement = (
        'self.C_d[period] = '
        'self.alpha_1[period]*self.YD[period] + '
        'self.alpha_2[period]*self.H_h[period-1]')
    assert FSIC.parser.code.identify_variables(statement) == (
        {'endogenous': ['self.C_d'],
         'exogenous': list(sorted(['self.alpha_1',
                                   'self.YD',
                                   'self.alpha_2',
                                   'self.H_h']))})


def test_identify_variables_one_exogenous_variable_no_prefix():
    statement = 'C_s[0] = C_d[0]'
    assert FSIC.parser.code.identify_variables(statement, prefix=r'\b') == (
        {'endogenous': ['C_s'],
         'exogenous': ['C_d']})


def test_identify_variables_multiple_exogenous_variables_no_prefix():
    statement = (
        'C_d[period] = '
        'alpha_1[period] * YD[period] + '
        'alpha_2[period] * H_h[period-1]')
    assert FSIC.parser.code.identify_variables(statement, prefix=r'\b') == (
        {'endogenous': ['C_d'],
         'exogenous': list(sorted(['alpha_1',
                                   'YD',
                                   'alpha_2',
                                   'H_h']))})


def test_identify_variables_multiple_exogenous_variables_with_suffix():
    statement = (
        'self.C_d[period] = '
        'self.alpha_1[period] * self.YD[period] + '
        'self.alpha_2[period] * self.H_h[period-1]')
    assert FSIC.parser.code.identify_variables(
        statement,
        suffix=r'\[.+?\]') == (
        {'endogenous': ['self.C_d[period]'],
         'exogenous': list(sorted(['self.alpha_1[period]',
                                   'self.YD[period]',
                                   'self.alpha_2[period]',
                                   'self.H_h[period-1]']))})


def test_identify_variables_multiple_lines():
    statement = '\n'.join([
        'self.C_s = self.C_d',
        'self.G_s = self.G_d',
        'self.T_s = self.T_d',
        'self.N_s = self.N_d', ])
    assert FSIC.parser.code.identify_variables(statement) == (
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
    assert FSIC.parser.code.identify_variables(statement) == (
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
    assert FSIC.parser.code.identify_variables(
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


def test_substitute():
    statement = 'C_d = C_d[-1]'
    expected = 'self.C_d[period] = self.C_d[period-1]'
    output = statement
    output = FSIC.parser.code.substitute(
        re.compile(r'(\b[A-z_]\w*)\b'),
        lambda x: 'self.' + x.groups()[0],
        output)
    output = FSIC.parser.code.substitute(
        re.compile(r'\[\s*([\d+-]+)\s*\]'),
        lambda x: '[period' + x.groups()[0] + ']',
        output)
    output = FSIC.parser.code.substitute(
        re.compile(r'(self[.][A-z_]\w*\b)(?!\[)'),
        lambda x: x.groups()[0] + '[period]',
        output)
    assert output == expected


def test_substitute_ignore_keywords():
    statement = 'C_d is C_d[-1]'
    expected = 'C_d is C_d[-1]'
    output = FSIC.parser.code.substitute(
        re.compile(r'\bis\b'),
        lambda x: 'is not',
        statement)
    assert output == expected


def test_substitute_include_keywords():
    statement = 'C_d is C_d[-1]'
    expected = 'C_d is not C_d[-1]'
    output = FSIC.parser.code.substitute(
        re.compile(r'\bis\b'),
        lambda x: 'is not',
        statement,
        ignore_keywords=False)
    assert output == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
