# -*- coding: utf-8 -*-
"""
test_model
==========
Test FSIC `Model` class.

"""

from pandas import PeriodIndex
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

import nose
from nose.tools import raises

from FSIC.classes.model import Model


class TestModel(Model):
    VARIABLES = list('YCIGXM')
    START_OFFSET = 5
    END_OFFSET = 5

class TestModelConv(TestModel):
    CONVERGENCE_VARIABLES = list('Y')


def test_initialise_period_index():
    xp = DataFrame({'Y': 0.0, 'C': 0.0, 'I': 0.0, 'G': 0.0, 'X': 0.0, 'M': 0.0,
                    'iterations': -1, 'converged': False, 'status': '-'},
                   index=PeriodIndex(start=1990, end=2020))

    model = TestModel(1990, 2020)
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

    model.initialise(solve_from=1995, solve_to=2015)
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

    model.initialise(1990, 2020, variables=list('YCIG'))
    assert_frame_equal(
        model.data.reindex(columns=xp.drop(list('XM'), axis=1).columns),
        xp.drop(list('XM'), axis=1))

    model.initialise(1990, 2020, parameters=list('YCIG'))
    assert_frame_equal(
        model.data.reindex(columns=xp.drop(list('XM'), axis=1).columns),
        xp.drop(list('XM'), axis=1))

    model.initialise(1990, 2020, errors=list('YCIG'))
    assert_frame_equal(
        model.data.reindex(columns=xp.drop(list('XM'), axis=1).columns),
        xp.drop(list('XM'), axis=1))

    model.initialise(data=xp)
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

    model.initialise(1990, 2020, data=xp.ix[1995:2000, :])
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

def test_initialise_integer_index():
    xp = DataFrame({'Y': 0.0, 'C': 0.0, 'I': 0.0, 'G': 0.0, 'X': 0.0, 'M': 0.0,
                    'iterations': -1, 'converged': False, 'status': '-'},
                   index=range(-10, 11))

    model = TestModel(-10, 10)
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

    model.initialise(-10, 10, convergence_variables=['Y'])
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

    model = TestModelConv(solve_from=-5, solve_to=5)
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

    model.initialise(data=xp)
    assert_frame_equal(model.data.reindex(columns=xp.columns), xp)

@raises(ValueError)
def test_initialise_errors_start():
    model = Model().initialise(end=10)

@raises(ValueError)
def test_initialise_errors_end():
    model = Model().initialise(start=-10)


if __name__ == '__main__':
    nose.runmodule()
