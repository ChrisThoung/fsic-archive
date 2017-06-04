# -*- coding: utf-8 -*-
"""
test_equation
=============
Test FSIC `Equation` class for single equations.

"""

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

import nose
from fsic.classes.equation import Equation


def test_equation():
    expression = 'C_d = {alpha_0} + max({alpha_1} * YD[0], C_d[-1]) + {alpha_2} * H_h[-1] + $I2000$ + <epsilon>'

    xp_terms = DataFrame.from_dict({
        'endogenous_0': {'raw': 'C_d', 'name': 'C_d', 'type': 'endogenous', 'index': 0, 'normalised': 'C_d'},
        'parameter_0': {'raw': '{alpha_0}', 'name': 'alpha_0', 'type': 'parameter', 'index': 0, 'normalised': 'alpha_0'},
        'function_0': {'raw': 'max', 'name': 'max', 'type': 'function', 'index': 0, 'normalised': 'max'},
        'parameter_1': {'raw': '{alpha_1}', 'name': 'alpha_1', 'type': 'parameter', 'index': 0, 'normalised': 'alpha_1'},
        'exogenous_0': {'raw': 'YD[0]', 'name': 'YD', 'type': 'exogenous', 'index': 0, 'normalised': 'YD'},
        'exogenous_1': {'raw': 'C_d[-1]', 'name': 'C_d', 'type': 'exogenous', 'index': -1, 'normalised': 'C_d[-1]'},
        'parameter_2': {'raw': '{alpha_2}', 'name': 'alpha_2', 'type': 'parameter', 'index': 0, 'normalised': 'alpha_2'},
        'exogenous_2': {'raw': 'H_h[-1]', 'name': 'H_h', 'type': 'exogenous', 'index': -1, 'normalised': 'H_h[-1]'},
        'automatic_0': {'raw': '$I2000$', 'name': 'I2000', 'type': 'automatic', 'index': 0, 'normalised': 'I2000'},
        'error_0': {'raw': '<epsilon>', 'name': 'epsilon', 'type': 'error', 'index': 0, 'normalised': 'epsilon'}},
                                   orient='index')
    xp_template = '{endogenous_0} = {parameter_0} + {function_0}({parameter_1} * {exogenous_0}, {exogenous_1}) + {parameter_2} * {exogenous_2} + {automatic_0} + {error_0}'
    xp_symbols = DataFrame.from_dict({
        'C_d': {'type': 'endogenous', 'min': -1, 'max': 0},
        'H_h': {'type': 'exogenous', 'min': -1, 'max': -1},
        'I2000': {'type': 'automatic', 'min': 0, 'max': 0},
        'YD': {'type': 'exogenous', 'min': 0, 'max': 0},
        'alpha_0': {'type': 'parameter', 'min': 0, 'max': 0},
        'alpha_1': {'type': 'parameter', 'min': 0, 'max': 0},
        'alpha_2': {'type': 'parameter', 'min': 0, 'max': 0},
        'epsilon': {'type': 'error', 'min': 0, 'max': 0},
        'max': {'type': 'function', 'min': 0, 'max': 0}},
                                     orient='index')

    eqn = Equation(expression)
    assert_frame_equal(eqn.terms, xp_terms.reindex(columns=eqn.terms.columns))
    assert eqn.template == xp_template
    assert_frame_equal(eqn.symbols.reindex(index=xp_symbols.index, columns=xp_symbols.columns),
                       xp_symbols)

def test_equation_power():
    # Check that '**' is left unchanged, not converted to '* *'
    expression = 'y = x ** 2'
    eqn = Equation(expression)
    assert eqn.template.format(**eqn.terms['normalised']) == expression

def test_equation_magic():
    a = Equation('H_h = H_h[-1] + YD - C_d')
    b = Equation('H_h[0] = H_h[-1] + YD[0] - C_d[0]')
    c = Equation('H_s = H_s + G_d - T_d')
    d = Equation('C_s = C_d')
    assert a == b
    assert not a.__eq__(b, strict=True)
    b.symbols.ix[0, 'max'] = 1
    assert a != b
    assert b != c
    assert c != d

def test_equation_initialise():
    consumption = Equation('C = ({alpha_1} * YD) + ({alpha_2} * H[-1])')
    consumption.initialise(index='ABCDEFG')

    assert_frame_equal(DataFrame(consumption.data),
                       DataFrame({v: 0.0
                                  for v in ['C', 'YD', 'H', 'alpha_1', 'alpha_2']},
                                 index=list('ABCDEFG')))

    consumption.alpha_1 = 0.6
    consumption.alpha_2 = 0.4

    assert_frame_equal(DataFrame(consumption.data),
                       DataFrame({'C': 0.0,
                                  'YD': 0.0,
                                  'H': 0.0,
                                  'alpha_1': 0.6,
                                  'alpha_2': 0.4},
                                index=list('ABCDEFG')))

def test_equation_solve_script():
    consumption = Equation('C = ({alpha_1} * YD) + ({alpha_2} * H[-1])')
    consumption.initialise(index='ABCDEFG')

    consumption.alpha_1 = 0.6
    consumption.alpha_2 = 0.4

    consumption.YD['B':] = 80.0
    consumption.H = 80.0

    for period in consumption.span():
        consumption.solve(period)

    assert_frame_equal(DataFrame(consumption.data),
                       DataFrame({'C': [0.0] + ([80.0] * 6),
                                  'YD': [0.0] + ([80.0] * 6),
                                  'H': [80.0] * 7,
                                  'alpha_1': 0.6,
                                  'alpha_2': 0.4},
                                index=list('ABCDEFG')))


if __name__ == '__main__':
    nose.runmodule()
