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

def test_getitem_single_column():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')})
    assert list(frame['X'].values()) == list(range(5))

def test_getitem_column_range():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')})
    assert_frame_equal(DataFrame(frame['Y':'Z']),
                       DataFrame({'Y': range(0, 10, 2),
                                  'Z': range(0, 15, 3)},
                                 index=list('ABCDE')))

def test_getitem_row_col_range():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')})
    assert_frame_equal(DataFrame(frame['B':'D', 'Y':'Z']),
                       DataFrame({'Y': range(2, 8, 2),
                                  'Z': range(3, 12, 3)},
                                 index=list('BCD')))

def test_setitem_add_column():
    frame = Frame({'X': Variable(range(5), index='ABCDE'),
                   'Y': Variable(range(0, 10, 2), index='ABCDE'),
                   'Z': Variable(range(0, 15, 3), index='ABCDE')})
    assert_frame_equal(DataFrame(frame),
                       DataFrame({'X': range(5),
                                  'Y': range(0, 10, 2),
                                  'Z': range(0, 15, 3)},
                                 index=list('ABCDE')))

    frame['F'] = 0
    assert list(frame['F'].values()) == [0] * 5
    assert_frame_equal(DataFrame(frame),
                       DataFrame({'X': range(5),
                                  'Y': range(0, 10, 2),
                                  'Z': range(0, 15, 3),
                                  'F': [0] * 5},
                                 index=list('ABCDE'))[list('XYZF')])


if __name__ == '__main__':
    nose.runmodule()
