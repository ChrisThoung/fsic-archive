# -*- coding: utf-8 -*-
"""
test_order
==========
Example equations come from Model SIM, from Chapter 3 of Godley and Lavoie
(2007).

"""


from nose.tools import raises, assert_warns

import FSIC.optimise.order


def test_recursive_empty():
    assert FSIC.optimise.order.recursive([]) == []


def test_recursive_single():
    unchanged = ['self.C_s[period] = self.C_d[period]']
    assert FSIC.optimise.order.recursive(unchanged) == unchanged


def test_recursive_simple():
    equations = [
        'self.Y[period] = self.C_s[period] + self.G_s[period]',
        'self.C_s[period] = self.C_d[period]',
    ]
    reordered = [
        'self.C_s[period] = self.C_d[period]',
        'self.Y[period] = self.C_s[period] + self.G_s[period]',
    ]
    assert FSIC.optimise.order.recursive(equations) == reordered


def test_recursive():
    equations = [
        'self.C_d[period] = self.alpha_1[period] * self.YD[period] + self.alpha_2[period] * self.H_h[period-1]',
        'self.C_s[period] = self.C_d[period]',
        'self.G_s[period] = self.G_d[period]',
        'self.T_s[period] = self.T_d[period]',
        'self.N_s[period] = self.N_d[period]',
        'self.H_s[period] = self.H_s[period-1] + self.G_d[period] - self.T_d[period]',
        'self.H_h[period] = self.H_h[period-1] + self.YD[period] - self.C_d[period]',
        'self.Y[period] = self.C_s[period] + self.G_s[period]',
        'self.N_d[period] = self.Y[period] / self.W[period]',
        'self.YD[period] = self.W[period] * self.N_s[period] - self.T_s[period]',
        'self.T_d[period] = self.theta[period] * self.W[period] * self.N_s[period]',
    ]
    reordered = [
        'self.G_s[period] = self.G_d[period]',
        'self.H_s[period] = self.H_s[period-1] + self.G_d[period] - self.T_d[period]',
        'self.C_s[period] = self.C_d[period]',
        'self.Y[period] = self.C_s[period] + self.G_s[period]',
        'self.N_d[period] = self.Y[period] / self.W[period]',
        'self.N_s[period] = self.N_d[period]',
        'self.T_d[period] = self.theta[period] * self.W[period] * self.N_s[period]',
        'self.T_s[period] = self.T_d[period]',
        'self.YD[period] = self.W[period] * self.N_s[period] - self.T_s[period]',
        'self.C_d[period] = self.alpha_1[period] * self.YD[period] + self.alpha_2[period] * self.H_h[period-1]',
        'self.H_h[period] = self.H_h[period-1] + self.YD[period] - self.C_d[period]',
    ]
    assert FSIC.optimise.order.recursive(equations) == reordered


@raises(ValueError)
def test_make_graph_error_zero_endogenous_variables():
    FSIC.optimise.order.make_graph([' = 0.0'])


@raises(ValueError)
def test_make_graph_error_multiple_endogenous_variables():
    FSIC.optimise.order.make_graph(['self.C_d[period] self.G_s[period] = 0.0'])


def test_make_graph_warning_duplicate_endogenous_variable():
    with assert_warns(Warning) as cm:
        FSIC.optimise.order.make_graph([
            'self.H_s[period] = self.H_s[period-1] + self.G_d[period] - self.T_d[period]',
            'self.H_h[period] = self.H_h[period-1] + self.YD[period] - self.C_d[period]',
            'self.H_h[period] = self.H_s[period]'])
    assert str(cm.warning) == 'An endogenous variable appears as the left hand-side variable in more than one equation'


if __name__ == '__main__':
    import nose
    nose.runmodule()
