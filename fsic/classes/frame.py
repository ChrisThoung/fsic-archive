# -*- coding: utf-8 -*-
"""
frame
=====
Dataframe-like object to store 'columns' of `Variable` objects (aping elements
of the behaviour of the `pandas` `DataFrame` class).

"""

from collections import OrderedDict

from fsic.classes.variable import Variable


class Frame(OrderedDict):
    """`OrderedDict`-based container for `Variable` objects."""

    def __init__(self, data=None):
        if data is not None:
            super().update(data)
