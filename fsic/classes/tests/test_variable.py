# -*- coding: utf-8 -*-
"""
test_variable
=============
Test FSIC `Variable` class.

"""

import nose
from nose.tools import raises

from fsic.classes.variable import Variable


def test_init():
    assert (list(Variable(range(10)).items()) ==
            list(zip(range(10), range(10))))
    assert (list(Variable(range(7), 'ABCDEFG').items()) ==
            list(zip('ABCDEFG', range(7))))
    assert (list(Variable(*zip(*zip(range(7), 'ABCDEFG'))).items()) ==
            list(zip('ABCDEFG', range(7))))
    assert (list(Variable('A', range(10)).items()) ==
            list(zip(range(10), ['A'] * 10)))
    assert (list(Variable(20, 'ABCDEFG').items()) ==
            list(zip('ABCDEFG', [20] * 7)))


if __name__ == '__main__':
    nose.runmodule()
