# -*- coding: utf-8 -*-
"""
test_frame
==========
Test FSIC `Frame` class.

"""

from collections import OrderedDict

import nose
from nose.tools import raises

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from fsic import Variable, Frame


def test_init_empty():
    frame = Frame()
    assert len(frame) == 0

def test_init_1():
    data = OrderedDict()
    data['X'] = Variable(range(5))
    data['Y'] = Variable(range(0, 10, 2))
    data['Z'] = Variable(range(0, 15, 3))

    frame = Frame(data)

    assert_frame_equal(DataFrame(frame),
                       DataFrame({'X': range(5),
                                  'Y': range(0, 10, 2),
                                  'Z': range(0, 15, 3)}))

def test_init_2():
    data = OrderedDict()
    data['X'] = Variable(range(5), index='ABCDE')
    data['Y'] = Variable(range(0, 10, 2), index='ABCDE')
    data['Z'] = Variable(range(0, 15, 3), index='ABCDE')

    frame = Frame(data)

    assert_frame_equal(DataFrame(frame),
                       DataFrame({'X': range(5),
                                  'Y': range(0, 10, 2),
                                  'Z': range(0, 15, 3)},
                                 index=list('ABCDE')))

def test_slice_single():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')},
                  sort=True)
    assert list(frame['X'].values()) == list(range(5))

def test_slice_single_range():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')},
                  sort=True)
    assert_frame_equal(DataFrame(frame['Y':'Z']),
                       DataFrame({'Y': range(0, 10, 2),
                                  'Z': range(0, 15, 3)},
                                 index=list('ABCDE')))

def test_slice_both_ranges():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')},
                  sort=True)
    assert_frame_equal(DataFrame(frame['B':'D', 'Y':'Z']),
                       DataFrame({'Y': range(2, 8, 2),
                                  'Z': range(3, 12, 3)},
                                 index=list('BCD')))


if __name__ == '__main__':
    nose.runmodule()
