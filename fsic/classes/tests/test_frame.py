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
    data['A'] = Variable(range(5))
    data['B'] = Variable(range(0, 10, 2))
    data['C'] = Variable(range(0, 15, 3))

    frame = Frame(data)

    assert_frame_equal(DataFrame(frame),
                       DataFrame({'A': range(5),
                                  'B': range(0, 10, 2),
                                  'C': range(0, 15, 3)}))

def test_init_2():
    data = OrderedDict()
    data['A'] = Variable(range(5), index='ABCDE')
    data['B'] = Variable(range(0, 10, 2), index='ABCDE')
    data['C'] = Variable(range(0, 15, 3), index='ABCDE')

    frame = Frame(data)

    assert_frame_equal(DataFrame(frame),
                       DataFrame({'A': range(5),
                                  'B': range(0, 10, 2),
                                  'C': range(0, 15, 3)},
                                 index=list('ABCDE')))


if __name__ == '__main__':
    nose.runmodule()
