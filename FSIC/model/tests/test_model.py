# -*- coding: utf-8 -*-


import os

from nose.tools import with_setup, raises

import numpy as np
from pandas import Series, DataFrame
import pandas as pd
from pandas.util.testing import assert_frame_equal

from FSIC.model.model import Model
from FSIC.settings import dtype


test_dir = os.path.dirname(__file__)


index_min = -50
index_max = 50


def setup():
    # Initialise a new Model object
    global model
    model = Model()
    # Initialise model variables
    temp = pd.read_csv(
        os.path.join(test_dir, 'data', 'table.csv'),
        index_col='index',
        dtype=dtype)
    for c in temp.columns:
        exec('model.%s = Series(0, index=range(%d, %d), dtype=dtype)' %
             (c, index_min, index_max + 1))


@with_setup(setup)
def test_read_data():
    input = os.path.join(test_dir, 'data', 'table.csv')
    # Read input data directly
    expected = pd.read_csv(input, index_col='index', dtype=dtype)
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


if __name__ == '__main__':
    import nose
    nose.runmodule()
