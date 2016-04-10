# -*- coding: utf-8 -*-
"""
test_utilities
==============
Test FSIC utility functions (where not tested elsewhere).

"""

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

import nose
from nose.tools import raises

from FSIC import Equation
from FSIC.exceptions import SpecificationError
from FSIC.utilities import merge_frames, make_comparison_function


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

    assert_frame_equal(symbols, xp.reindex(columns=symbols.columns))


def test_make_comparison_function():
    compare = make_comparison_function('abcd')
    assert compare('c', 'b') == 'b'

@raises(SpecificationError)
def test_make_comparison_function_specification_error():
    compare = make_comparison_function('abcd', 'efg')
    compare('a', 'e')


if __name__ == '__main__':
    nose.runmodule()
