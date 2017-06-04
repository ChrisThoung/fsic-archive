# -*- coding: utf-8 -*-
"""
frame
=====
Dataframe-like object to store 'columns' of `Variable` objects (aping elements
of the behaviour of the `pandas` `DataFrame` class).

"""

from collections import OrderedDict
from collections.abc import Container
import itertools

from fsic.classes.variable import Variable


class Frame(OrderedDict):
    """`OrderedDict`-based container for `Variable` objects."""

    CONTAINER = Variable

    def __init__(self, data=None, sort=True):
        if data is not None:
            if sort:
                for k in sorted(data):
                    super().__setitem__(k, data[k])
            else:
                super().update(data)

    _unpack_slice = Variable._unpack_slice
    _unpack_slice_to_labels = Variable._unpack_slice_to_labels

    def __getitem__(self, key):
        if type(key) is slice:
            column_labels = list(self._unpack_slice_to_labels(key))
            item = self.__class__(zip(column_labels, map(self.__getitem__, column_labels)), sort=False)
        elif type(key) is tuple:
            if len(key) != 2:
                raise KeyError('Only slicing up to two dimensions is supported')

            def filter_col(container):
                return self.CONTAINER(
                    container[key[0]],
                    container._unpack_slice_to_labels(key[0]))

            # Select columns...
            column_labels = list(self._unpack_slice_to_labels(key[1]))
            columns = map(self.__getitem__, column_labels)

            # ...then filter by row
            filtered_columns = map(filter_col, columns)
            item = self.__class__(zip(column_labels, filtered_columns), sort=False)
        else:
            item = super().__getitem__(key)

        return item

    def __setitem__(self, key, value):
        if type(key) is slice:
            raise NotImplementedError
        elif type(key) is tuple:
            raise NotImplementedError
        else:
            if not isinstance(value, Container) or isinstance(value, range):
                index = None

                if len(self):
                    index = next(iter(self.values())).keys()

                value = self.CONTAINER(value, index)

            super().__setitem__(key, value)
