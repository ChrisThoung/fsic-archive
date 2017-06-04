# -*- coding: utf-8 -*-
"""
frame
=====
Dataframe-like object to store 'columns' of `Variable` objects (aping elements
of the behaviour of the `pandas` `DataFrame` class).

"""

from collections import OrderedDict
import itertools

from fsic.classes.variable import Variable


class Frame(OrderedDict):
    """`OrderedDict`-based container for `Variable` objects."""

    CONTAINER = Variable

    def __init__(self, data=None, sort=False):
        if data is not None:
            if sort:
                for k in sorted(data):
                    super().__setitem__(k, data[k])
            else:
                super().update(data)

    def _unpack_slice(self, slice_):
        find = list(self.keys()).index

        start = 0 if slice_.start is None else find(slice_.start)
        stop = len(self) if slice_.stop is None else find(slice_.stop) + 1
        step = 1 if slice_.step is None else slice_.step

        return start, stop, step

    def __getitem__(self, key):
        if type(key) is slice:
            start, stop, step = self._unpack_slice(key)
            labels = list(itertools.islice(self.keys(), start, stop, step))
            item = self.__class__(zip(labels, map(self.__getitem__, labels)))
        elif type(key) is tuple:
            if len(key) != 2:
                raise KeyError('Only slicing up to two dimensions is supported')

            def filter_col(container):
                return self.CONTAINER(
                    container[key[0]],
                    container._unpack_slice_to_labels(key[0]))

            # Select columns...
            start, stop, step = self._unpack_slice(key[1])
            column_labels = list(itertools.islice(self.keys(), start, stop, step))
            columns = map(self.__getitem__, column_labels)

            # ...then filter by row
            filtered_columns = map(filter_col, columns)
            item = self.__class__(zip(column_labels, filtered_columns))
        else:
            item = super().__getitem__(key)

        return item
