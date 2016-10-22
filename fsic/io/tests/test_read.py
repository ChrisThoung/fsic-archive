# -*- coding: utf-8 -*-
"""
test_read
=========
Test FSIC `read()` function.

"""

import os

import numpy as np
from pandas import PeriodIndex
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from fsic.exceptions import FSICError
from fsic.io.api import read

import nose
from nose.tools import raises


def path(name):
    return os.path.join(os.path.split(__file__)[0], 'data', name)


def test_read_ab():
    expected = DataFrame({'A': [0] * 16 + [np.nan] * 4,
                          'B': [0] * 16 + [np.nan] * 4,
                          'C': [0] * 16 + [np.nan] * 4,
                          'D': [np.nan] * 4 + [0.25] * 16,
                          'E': [np.nan] * 4 + [0.25] * 16,
                          'F': [np.nan] * 4 + [0.25] * 16,
                          'G': [np.nan] * 4 + [0.25] * 16, },
                         index=['{}Q{}'.format(y, q)
                                for y in range(2000, 2005)
                                for q in range(1, 5)])
    assert_frame_equal(read([path('{}.csv'.format(a)) for a in 'ab'], index_col=0),
                       expected)

def test_read_ac():
    expected = DataFrame({'A': 0.5,
                          'B': [0.0] * 16 + [np.nan] * 8,
                          'C': 0.5,
                          'E': 0.5,
                          'G': 0.5, },
                         index=['{}Q{}'.format(y, q)
                                for y in range(2000, 2006)
                                for q in range(1, 5)])
    assert_frame_equal(read([path('{}.csv'.format(a)) for a in 'ac'], index_col=0),
                       expected)

def test_read_ae():
    expected = DataFrame({'A': [0.0] * 8 + [1.0] * 16,
                          'B': [0.0] * 8 + [1.0] * 16,
                          'C': [0.0] * 8 + [1.0] * 16, },
                         index=['{}Q{}'.format(y, q)
                                for y in range(2000, 2006)
                                for q in range(1, 5)])
    assert_frame_equal(read([path('{}.csv'.format(a)) for a in 'ae'], index_col=0),
                       expected)


@raises(ValueError)
def test_read_input_error():
    read(123)

@raises(FSICError)
def test_read_ext_error_str():
    read('unknown_file_ext.xyz')

@raises(FSICError)
def test_read_ext_error_iterable():
    read([path('a.csv'), 'unknown_file_ext.xyz'])


if __name__ == '__main__':
    nose.runmodule()
