# -*- coding: utf-8 -*-
"""
test_utilities
==============
Test FSIC utility functions (where not tested elsewhere).

"""

from pandas import Series, DataFrame
from pandas import PeriodIndex
from pandas.util.testing import assert_series_equal, assert_frame_equal

import nose
from nose.tools import raises

from FSIC import Equation
from FSIC.exceptions import SpecificationError
from FSIC.utilities import merge_frames, make_comparison_function
from FSIC.utilities import time_trend, indicator_matrix


def test_merge_frames():
    xp = DataFrame.from_dict({
        'C_s': {'type': 'endogenous', 'min': 0, 'max': 0},
        'C_d': {'type': 'endogenous', 'min': 0, 'max': 0},
        'alpha_1': {'type': 'parameter', 'min': 0, 'max': 0},
        'YD': {'type': 'exogenous', 'min': 0, 'max': 0},
        'alpha_2': {'type': 'parameter', 'min': 0, 'max': 0},
        'H_h': {'type': 'endogenous', 'min': -1, 'max': 0}},
                             orient='index')

    comparison_functions = {
        'type': make_comparison_function(Equation.PRECEDENCE),
        'min': min,
        'max': max}

    data = ['C_s = C_d',
            'C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]',
            'H_h = H_h[-1] + YD - C_d']
    equations = [Equation(x) for x in data]
    symbols = merge_frames([e.symbols for e in equations],
                           comparison_functions)

    assert_frame_equal(symbols.reindex(index=xp.index, columns=xp.columns), xp)


def test_make_comparison_function():
    compare = make_comparison_function('abcd')
    assert compare('c', 'b') == 'b'

@raises(SpecificationError)
def test_make_comparison_function_specification_error():
    compare = make_comparison_function('abcd', 'efg')
    compare('a', 'e')


def test_time_trend():
    expected = Series(range(7), index=list('ABCDEFG'))
    assert_series_equal(time_trend(tuple('ABCDEFG')), expected)
    assert_series_equal(time_trend(list('ABCDEFG')), expected)

    expected = Series(range(-2, 5), index=list('ABCDEFG'))
    assert_series_equal(time_trend(list('ABCDEFG'), iloc=-5), expected)
    assert_series_equal(time_trend(list('ABCDEFG'), loc='C'), expected)

    expected = Series(range(-4, 8), index=PeriodIndex(start='1999Q1', end='2001Q4'))
    assert_series_equal(time_trend(expected.index, iloc=4), expected)
    assert_series_equal(time_trend(expected.index, loc='2000Q1'), expected)

    expected = Series(range(4, -8, -1), index=PeriodIndex(start='1999Q1', end='2001Q4'))
    assert_series_equal(time_trend(expected.index, iloc=4, descending=True), expected)
    assert_series_equal(time_trend(expected.index, loc='2000Q1', descending=True), expected)

@raises(ValueError)
def test_time_trend_argument_error():
    time_trend(list('ABCDEFG'), iloc=2, loc='C')

@raises(AttributeError)
def test_time_trend_find_error():
    time_trend(1234, loc=2)


def test_indicator_matrix():
    expected = DataFrame([[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0], ],
                         index=PeriodIndex(start='2000Q1', end='2000Q4'),
                         columns=['I{}Q{}'.format(2000, q) for q in range(1, 5)])
    assert_frame_equal(indicator_matrix(expected.index, kind='impulse'), expected)
    assert_frame_equal(indicator_matrix(expected.index, kind='impulse', drop_constants=True), expected)

    expected = DataFrame([[1.0, 0.0, 0.0, 0.0],
                          [1.0, 1.0, 0.0, 0.0],
                          [1.0, 1.0, 1.0, 0.0],
                          [1.0, 1.0, 1.0, 1.0], ],
                         index=PeriodIndex(start='2000Q1', end='2000Q4'),
                         columns=['S{}Q{}'.format(2000, q) for q in range(1, 5)])
    assert_frame_equal(indicator_matrix(expected.index, kind='step'), expected)
    assert_frame_equal(indicator_matrix(expected.index, kind='step', drop_constants=True), expected.drop('S2000Q1', axis=1))

    expected = DataFrame([[0.0, 0.0, 0.0, 0.0],
                          [1.0, 0.0, 0.0, 0.0],
                          [2.0, 1.0, 0.0, 0.0],
                          [3.0, 2.0, 1.0, 0.0], ],
                         index=PeriodIndex(start='2000Q1', end='2000Q4'),
                         columns=['T{}Q{}'.format(2000, q) for q in range(1, 5)])
    assert_frame_equal(indicator_matrix(expected.index, kind='trend'), expected)
    assert_frame_equal(indicator_matrix(expected.index, kind='trend', drop_constants=True), expected.drop('T2000Q4', axis=1))

    expected = DataFrame([[0.0, 1.0, 2.0, 3.0],
                          [1.0, 2.0, 3.0, 3.0],
                          [2.0, 3.0, 3.0, 3.0],
                          [3.0, 3.0, 3.0, 3.0], ],
                         index=PeriodIndex(start='2000Q1', end='2000Q4'),
                         columns=['P{}Q{}'.format(2000, q) for q in range(1, 5)])
    assert_frame_equal(indicator_matrix(expected.index, kind='plateau'), expected)
    assert_frame_equal(indicator_matrix(expected.index, kind='plateau', drop_constants=True), expected.drop('P2000Q4', axis=1))

@raises(ValueError)
def test_indicator_matrix_kind_error():
    indicator_matrix(range(10), kind='invalid')


if __name__ == '__main__':
    nose.runmodule()
