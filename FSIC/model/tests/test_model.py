# -*- coding: utf-8 -*-


from random import uniform
import os

from nose.tools import with_setup, raises

import numpy as np
from pandas import PeriodIndex
from pandas import Series, DataFrame
import pandas as pd
from pandas.util.testing import assert_frame_equal

from FSIC.model.model import Model
from FSIC.settings import DTYPE


test_dir = os.path.dirname(__file__)


index_min = -50
index_max = 50


def setup_base():
    # Initialise a new Model object
    global model
    model = Model()
    # Initialise model variables
    temp = pd.read_csv(
        os.path.join(test_dir, 'data', 'table.csv'),
        index_col='index',
        dtype=DTYPE)
    for c in temp.columns:
        exec('model.%s = Series(0, index=range(%d, %d), dtype=DTYPE)' %
             (c, index_min, index_max + 1))


class Derived(Model):

    def initialise(self, span, solve_from=None, solve_to=None, default=0.0):
        # Store arguments
        self.span = span
        self.solve_from = solve_from
        self.solve_to = solve_to
        # Initialise `iter`
        self.iter = Series(default, index=self.span, dtype=DTYPE)
        # Initialise model variables
        self.C = Series(default, index=self.span, dtype=DTYPE)
        self.I = Series(default, index=self.span, dtype=DTYPE)
        self.G = Series(default, index=self.span, dtype=DTYPE)
        self.X = Series(default, index=self.span, dtype=DTYPE)
        self.M = Series(default, index=self.span, dtype=DTYPE)
        self.Y = Series(default, index=self.span, dtype=DTYPE)
        # Update solution-state variables
        self.initialised = True
        self.solved = False

    def get_endogenous_variable_values(self, period):
        values = {}
        values['Y'] = self.Y[period]
        return Series(values)

    def solve_equations(self, period):
        self.Y[period] = (
            self.C[period] +
            self.I[period] +
            self.G[period] +
            self.X[period] -
            self.M[period])

def setup_derived():
    global model
    model = Derived()


class DerivedNonConvergence(Derived):

    def solve_equations(self, period):
        self.X[period] = uniform(0, 100)
        self.Y[period] = (
            self.C[period] +
            self.I[period] +
            self.G[period] +
            self.X[period] -
            self.M[period])

def setup_derived_non_convergence():
    global model
    model = DerivedNonConvergence()


@with_setup(setup_base)
def test_not_initialised_or_solved_base():
    assert model.initialised is False
    assert model.solved is False


@with_setup(setup_derived)
def test_not_initialised_or_solved_derived():
    assert model.initialised is False
    assert model.solved is False


@with_setup(setup_base)
def test_read_data():
    input = os.path.join(test_dir, 'data', 'table.csv')
    # Read input data directly
    expected = pd.read_csv(input, index_col='index', dtype=DTYPE)
    # Read input data using `model`
    model.read_data(input)
    columns = ['\'%s\': model.%s' % (c, c) for c in expected.columns]
    result = eval('DataFrame({%s})' % ', '.join(columns))
    result = result[expected.columns]
    result = result.reset_index()
    result.set_index(keys=result['index'].astype(int), inplace=True)
    del result['index']
    # Extend `expected` to match contents of `model`
    expected = pd.concat(
        [DataFrame(
            0, index=range(index_min, 0),
            columns=expected.columns),
         expected,
         DataFrame(
             0, index=range(int(max(expected.index) + 1), index_max + 1),
             columns=expected.columns), ],
        axis=0)
    expected = expected.reset_index()
    expected.set_index(keys=expected['index'].astype(int), inplace=True)
    del expected['index']
    # Test
    assert_frame_equal(result, expected)


@with_setup(setup_derived)
def test_initialise_and_solve():
    # Initialise
    model.initialise(span=PeriodIndex(start='1954', end='2014'))
    assert model.initialised is True
    assert model.solved is False
    # Set values (note difference in Python list and pandas date indexing)
    model.C.ix[10:15] = 50
    model.M.ix['1964':'1968'] = 25
    # Solve
    model.solve()
    assert model.initialised is True
    assert model.solved is True
    # Check
    assert model.Y.ix[9] == 0
    assert model.Y.ix[10] == 25
    assert model.Y.ix[11] == 25
    assert model.Y.ix[12] == 25
    assert model.Y.ix[13] == 25
    assert model.Y.ix[14] == 25
    assert model.Y.ix[15] == 0
    for i in model.iter:
        assert not np.isnan(i)


@with_setup(setup_derived_non_convergence)
def test_no_convergence():
    model.initialise(span=PeriodIndex(start='1954', end='2014'))
    model.solve(max_iter=10)
    for i in model.iter:
        assert np.isnan(i)


@with_setup(setup_derived)
@raises(ValueError)
def test_solve_not_initialised_error():
    model.solve()


if __name__ == '__main__':
    import nose
    nose.runmodule()
