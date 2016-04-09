# -*- coding: utf-8 -*-
"""
test_utilities
==============
Test FSIC utility functions (where not tested elsewhere).

"""

import nose
from nose.tools import raises

from FSIC.exceptions import SpecificationError
from FSIC.utilities import make_comparison_function


def test_make_comparison_function():
    compare = make_comparison_function('abcd')
    assert compare('c', 'b') == 'b'

@raises(SpecificationError)
def test_make_comparison_function_specification_error():
    compare = make_comparison_function('abcd', 'efg')
    compare('a', 'e')


if __name__ == '__main__':
    nose.runmodule()
