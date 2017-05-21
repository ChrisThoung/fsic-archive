# -*- coding: utf-8 -*-
"""
test_variable
=============
Test FSIC `Variable` class.

"""

import nose
from nose.tools import raises

from fsic import Variable
from fsic.exceptions import DimensionError


def test_init_empty():
    assert len(Variable()) == 0
    assert len(list(Variable().keys())) == 0
    assert len(list(Variable().values())) == 0
    assert len(list(Variable().items())) == 0


def test_init_single_values_no_index():
    assert list(Variable(20).items()) == [(0, 20)]
    assert list(Variable('A').items()) == [(0, 'A')]

    assert list(Variable([20]).items()) == [(0, 20)]
    assert list(Variable(['A']).items()) == [(0, 'A')]

    assert list(Variable(['AB']).items()) == [(0, 'AB')]

def test_init_single_values_index():
    assert list(Variable(20, range(5)).items()) == list(zip(range(5), [20] * 5))
    assert list(Variable(20, 'ABCDEFG').items()) == list(zip('ABCDEFG', [20] * 7))

    assert list(Variable([20], range(5)).items()) == list(zip(range(5), [20] * 5))
    assert list(Variable([20], 'ABCDEFG').items()) == list(zip('ABCDEFG', [20] * 7))

    assert list(Variable('A', range(5)).items()) == list(zip(range(5), ['A'] * 5))
    assert list(Variable('A', 'ABCDEFG').items()) == list(zip('ABCDEFG', ['A'] * 7))

    assert list(Variable(['A'], range(5)).items()) == list(zip(range(5), ['A'] * 5))
    assert list(Variable(['A'], 'ABCDEFG').items()) == list(zip('ABCDEFG', ['A'] * 7))

def test_init_iterable_values_no_index():
    assert list(Variable(range(10)).items()) == list(zip(range(10), range(10)))
    assert list(Variable('ABCDEFG').items()) == list(zip(range(7), 'ABCDEFG'))

def test_init_iterable_values_index():
    assert list(Variable(range(7), 'ABCDEFG').items()) == list(zip('ABCDEFG', range(7)))
    assert list(Variable(*zip(*zip(range(7), 'ABCDEFG'))).items()) == list(zip('ABCDEFG', range(7)))


@raises(DimensionError)
def test_init_length_error1():
    Variable(range(10), 'ABCDEFG')

@raises(DimensionError)
def test_init_length_error2():
    Variable(range(5), 'ABCDEFG')


def test_simple_indexing():
    test_var = Variable(range(7), 'ABCDEFG')

    for i, a in enumerate('ABCDEFG'):
        assert test_var[a] == i

def test_slice_indexing():
    test_var = Variable(range(7), 'ABCDEFG')

    assert test_var['B':'D'] == [1, 2, 3]
    assert test_var[:'C'] == [0, 1, 2]
    assert test_var['E':] == [4, 5, 6]
    assert test_var[::2] == [0, 2, 4, 6]


if __name__ == '__main__':
    nose.runmodule()
