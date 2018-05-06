# -*- coding: utf-8 -*-
"""
test_model
==========
Test FSIC `Model` class.

"""

import os
import warnings

import numpy as np

from pandas import PeriodIndex
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
import pandas as pd

import nose
from nose.tools import raises

from fsic.classes.model import Model
from fsic.exceptions import FSICError


def standardise_integer_column_dtypes(frame):
    """Return a copy of `frame` with integer columns coerced to the (system) default integer type."""
    coerced = frame.copy()

    for name, dtype in frame.dtypes.items():
        if np.issubdtype(dtype, np.integer):
            coerced[name] = coerced[name].astype(int)

    return coerced


class NaNs(Model):
    VARIABLES = ['c', 'C', 'PC']

    def _solve_python_iteration(self, row):
        self.c.values[row] = (self.C.values[row] /
                              self.PC.values[row])

class Variables(Model):
    VARIABLES = list('YCIGXM')

class Accounting(Variables):
    CONVERGENCE_VARIABLES = list('Y')

    def _solve_python_iteration(self, row):
        self.Y.values[row] = (self.C.values[row] +
                              self.I.values[row] +
                              self.G.values[row] +
                              self.X.values[row] -
                              self.M.values[row])

class Dynamic(Accounting):
    START_OFFSET = 5
    END_OFFSET = 5


def test_initialise_period_index():
    xp = DataFrame({'Y': 0.0, 'C': 0.0, 'I': 0.0, 'G': 0.0, 'X': 0.0, 'M': 0.0,
                    'iterations': -1, 'converged': False, 'status': '-'},
                   index=PeriodIndex(start=1990, end=2020))

    model = Dynamic(1990, 2020)
    assert_frame_equal(standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
                       standardise_integer_column_dtypes(xp))

    model.initialise(solve_from=1995, solve_to=2015)
    assert_frame_equal(standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
                       standardise_integer_column_dtypes(xp))

    model.initialise(1990, 2020, variables=list('YCIG'))
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.drop(list('XM'), axis=1).columns)),
        standardise_integer_column_dtypes(xp.drop(list('XM'), axis=1)))

    model.initialise(1990, 2020, parameters=list('YCIG'))
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.drop(list('XM'), axis=1).columns)),
        standardise_integer_column_dtypes(xp.drop(list('XM'), axis=1)))

    model.initialise(1990, 2020, errors=list('YCIG'))
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.drop(list('XM'), axis=1).columns)),
        standardise_integer_column_dtypes(xp.drop(list('XM'), axis=1)))

    model.initialise(data=xp)
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
        standardise_integer_column_dtypes(xp))

    model.initialise(1990, 2020, data=xp.loc['1995':'2000', :])
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
        standardise_integer_column_dtypes(xp))

def test_initialise_period_index_from_int():
    data = DataFrame({'Y': 0.0, 'C': 0.0, 'I': 0.0, 'G': 0.0, 'X': 0.0, 'M': 0.0, },
                     index=range(1995, 2006))
    data.loc[2000, 'G'] = 20
    model = Variables(data=data)

    try:
        assert model.data.loc['2000', 'G'] == 20
    except AssertionError:
        print('Expected:')
        print(data)
        print('\nResult:')
        print(model.data[data.columns])
        raise

def test_initialise_integer_index():
    xp = DataFrame({'Y': 0.0, 'C': 0.0, 'I': 0.0, 'G': 0.0, 'X': 0.0, 'M': 0.0,
                    'iterations': -1, 'converged': False, 'status': '-'},
                   index=range(-10, 11))

    model = Variables(-10, 10)
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
        standardise_integer_column_dtypes(xp))

    model.initialise(-10, 10, convergence_variables=['Y'])
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
        standardise_integer_column_dtypes(xp))

    model = Dynamic(solve_from=-5, solve_to=5)
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
        standardise_integer_column_dtypes(xp))

    model = Model(solve_from=1, solve_to=1000)
    assert list(model.data.index.values) == list(range(1, 1001))

    model.initialise(data=xp)
    assert_frame_equal(
        standardise_integer_column_dtypes(model.data.reindex(columns=xp.columns)),
        standardise_integer_column_dtypes(xp))

def test_initialise_integer_index_with_zero():
    model = Model(0, 5)
    assert list(model.data.index) == list(range(6))

    model = Model(-5, 0)
    assert list(model.data.index) == list(range(-5, 1))

    model = Model(solve_from=0, solve_to=10)
    assert list(model.data.index) == list(range(11))

    model = Model(solve_from=-10, solve_to=0)
    assert list(model.data.index) == list(range(-10, 1))


def test_initialise_static_index():
    model = Model(index=['before', 'after'])
    assert model.data.index.tolist() == ['before', 'after']

@raises(FSICError)
def test_initialise_static_index_error():
    model = Dynamic(index=['before', 'after'])


@raises(ValueError)
def test_initialise_errors_start():
    model = Model().initialise(end=10)

@raises(ValueError)
def test_initialise_errors_end():
    model = Model().initialise(start=-10)


def test_property_get_set():
    model = Model(0, 10, variables=list('YCIG'))

    model.Y = 10
    assert model.Y.sum() == 110

    model.Y[5] = 50
    assert model.Y.sum() == 150

    model.G[3:5] = 20
    assert model.G.sum() == 40

@raises(RuntimeError)
def test_property_del_error():
    model = Model(0, 10, variables=list('YCIG'))
    del model.Y


@raises(RuntimeError)
def test_solve_before_initialise():
    model = Model()
    model.solve()

@raises(ValueError)
def test_solve_period_argument_error():
    model = Model(0, 10)
    model.solve(first=2, last=8, single=5)

def test_solve():
    model = Dynamic('2000Q1', '2005Q4')
    model.G = 20
    model.M = 10
    model.solve(single='2000Q1')
    model.solve(single='2005Q4', verbosity=1)
    model.solve()
    model.solve('2000Q2', '2000Q4', verbosity=1)
    assert sum(model.Y * model.iterations) == 380

def test_solve_copy_convergence():
    default = Dynamic('2000Q1', '2005Q4') ; default.G = 20 ; default.M = 10 ; default.solve()
    convergence = Dynamic('2000Q1', '2005Q4') ; convergence.G = 20 ; convergence.M = 10 ; convergence.solve(copy='convergence')
    assert_frame_equal(default.data[list('YCIGXM')], convergence.data[list('YCIGXM')])

    # Ensure that `convergence` solved at least as quickly as `default` and
    # that at least some periods solved quicker
    iterations = convergence.iterations - default.iterations
    assert (iterations <= 0).all()
    assert sum(iterations) < 0

@raises(NotImplementedError)
def test_solve_copy_endogenous():
    default = Dynamic('2000Q1', '2005Q4') ; default.G = 20 ; default.M = 10 ; default.solve()
    endogenous = Dynamic('2000Q1', '2005Q4') ; endogenous.G = 20 ; endogenous.M = 10 ; endogenous.solve(copy='endogenous')
    assert_frame_equal(default.data[list('YCIGXM')], endogenous.data[list('YCIGXM')])

    # Ensure that `endogenous` solved at least as quickly as `default` and
    # that at least some periods solved quicker
    iterations = endogenous.iterations - default.iterations
    assert (iterations <= 0).all()
    assert sum(iterations) < 0


def test_solve_static_single():
    model = Accounting(index=['before', 'after'])
    model.G = [20, 25]
    assert model.Y.tolist() == [0, 0]
    model.solve(single='before', verbosity=1)
    assert model.Y.tolist() == [20, 0]
    model.solve(single='after', verbosity=2)
    assert model.Y.tolist() == [20, 25]

def test_solve_static_all():
    model = Accounting(index=['before', 'after'])
    model.G = [20, 25]
    model.solve()
    assert model.Y.tolist() == [20, 25]

def test_solve_nans():
    # Check immediate halt each period in the event of a NaN propagating
    # through the system
    model = NaNs(0, 10)

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        model.solve(verbosity=2)

    assert model.data['c'].isnull().all()
    assert (model.data['status'] == 'N').all()
    assert (model.data['iterations'] == 1).all()


def test_initialise_from_data_and_solve():
    # Initialise a model from a dataset and solve
    data = pd.read_csv(os.path.join(os.path.split(__file__)[0],
                                    'data', 'annual.csv'),
                       index_col=0)

    input_data = data.copy()
    input_data['Y'] = 0

    model = Accounting(data=input_data)
    model.solve()

    assert_frame_equal(model.data[data.columns], data)


def test_make_spacing():
    model = Model(-10, 11)
    assert model._make_spacing() == ([False] * 5 + [True] +
                                     [False] * 4 + [True] +
                                     [False] * 4 + [True] +
                                     [False] * 4 + [True] +
                                     [False])
    model = Model(1990, 2011)
    assert model._make_spacing() == ([False] * 5 + [True] +
                                     [False] * 4 + [True] +
                                     [False] * 4 + [True] +
                                     [False] * 4 + [True] +
                                     [False])
    model = Model('1990', '2011')
    assert model._make_spacing() == ([False] * 5 + [True] +
                                     [False] * 4 + [True] +
                                     [False] * 4 + [True] +
                                     [False] * 4 + [True] +
                                     [False])
    model = Model('2000Q1', '2002Q4')
    assert model._make_spacing(range(4, 12)) == ([False] * 4 + [True] + [False] * 3)


if __name__ == '__main__':
    nose.runmodule()
