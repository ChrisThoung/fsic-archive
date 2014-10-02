# -*- coding: utf-8 -*-


import os

from nose.tools import with_setup, raises

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

from FSIC.model.model import Model


test_dir = os.path.dirname(__file__)


def setup():
    global model
    model = Model()


@with_setup(setup)
def test_read_data():
    input = os.path.join(test_dir, 'data', 'table.csv')
    model.read_data(input)
    expected = pd.read_csv(input, dtype=np.float64)
    assert_frame_equal(model.data, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule()
