# -*- coding: utf-8 -*-
"""
variable
========
Container based on standard-library `OrderedDict` class, augmented with
`pandas`-style indexing (aping the behaviour of the `Series` class).

"""

from collections import OrderedDict
from collections.abc import Iterable
import itertools


from fsic.exceptions import DimensionError


class Variable(OrderedDict):
    """`OrderedDict`-based container with `pandas` Series-style indexing."""

    def __init__(self, values=None, index=None):
        """Initialise object with values and index (keys).

        Parameters
        ----------
        values : constant or iterable, default `None`
        index : iterable, defaults to [0, 1, ...]

        Examples
        --------
        >>> Variable(20)
        Variable([(0, 20)])

        >>> Variable(['20'])
        Variable([(0, '20')])

        >>> Variable(range(5))
        Variable([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])

        >>> Variable([i * 2 for i in range(5)])
        Variable([(0, 0), (1, 2), (2, 4), (3, 6), (4, 8)])

        >>> Variable(0.0, 'ABCDEFG')
        Variable([('A', 0.0), ('B', 0.0), ('C', 0.0), ('D', 0.0), ('E', 0.0), ('F', 0.0), ('G', 0.0)])

        >>> Variable(range(7), 'ABCDEFG')
        Variable([('A', 0), ('B', 1), ('C', 2), ('D', 3), ('E', 4), ('F', 5), ('G', 6)])

        """
        if values is None and index is None:
            contents = zip((), ())
        else:
            if index is None:
                if isinstance(values, Iterable):
                    index = itertools.count()
                else:
                    values, index = [values], [0]
                contents = zip(index, values)
            else:
                if not isinstance(values, Iterable):
                    values = [values]

                if len(values) == 1:
                    contents = zip(index, itertools.cycle(values))
                else:
                    index, value = map(list, (index, values))
                    if len(index) != len(values):
                        raise DimensionError(
                            'Unequal argument lengths of '
                            '`values` ({}) and `index` ({})'.format(len(values),
                                                                    len(index)))
                    contents = zip(index, values)

        super().update(contents)


    def _unpack_slice(self, slice_):
        find = list(self.keys()).index

        start = 0 if slice_.start is None else find(slice_.start)
        stop = len(self) if slice_.stop is None else find(slice_.stop) + 1
        step = 1 if slice_.step is None else slice_.step

        return start, stop, step

    def __getitem__(self, key):
        """Augmented getter, aping `pandas` `Series`-style indexing.

        Examples
        --------
        >>> example_var = Variable(range(7), 'ABCDEFG')

        >>> example_var['A']
        0

        >>> example_var['B':'D']
        [1, 2, 3]

        >>> example_var[:'C']
        [0, 1, 2]

        >>> example_var['E':]
        [4, 5, 6]

        >>> example_var[::2]
        [0, 2, 4, 6]

        """
        if type(key) is slice:
            start, stop, step = self._unpack_slice(key)
            labels = itertools.islice(self.keys(), start, stop, step)
            item = list(map(self.__getitem__, labels))
        else:
            item = super().__getitem__(key)

        return item

    def __setitem__(self, key, value):
        """Augmented setter, aping `pandas` `Series`-style indexing.

        Examples
        --------
        >>> example_var = Variable(range(7), 'ABCDEFG')
        >>> example_var
        Variable([('A', 0), ('B', 1), ('C', 2), ('D', 3), ('E', 4), ('F', 5), ('G', 6)])

        >>> example_var['A'] = 10
        >>> example_var
        Variable([('A', 10), ('B', 1), ('C', 2), ('D', 3), ('E', 4), ('F', 5), ('G', 6)])

        >>> example_var['B':'D'] = 3, 2, 1
        >>> example_var
        Variable([('A', 10), ('B', 3), ('C', 2), ('D', 1), ('E', 4), ('F', 5), ('G', 6)])

        >>> example_var['C':] = 50
        >>> example_var
        Variable([('A', 10), ('B', 3), ('C', 50), ('D', 50), ('E', 50), ('F', 50), ('G', 50)])

        >>> example_var[:'C'] = -50
        >>> example_var
        Variable([('A', -50), ('B', -50), ('C', -50), ('D', 50), ('E', 50), ('F', 50), ('G', 50)])

        >>> example_var[::2] = 100
        >>> example_var
        Variable([('A', 100), ('B', -50), ('C', 100), ('D', 50), ('E', 100), ('F', 50), ('G', 100)])

        >>> example_var[::2] = [0, 2, 4, 6]
        >>> example_var
        Variable([('A', 0), ('B', -50), ('C', 2), ('D', 50), ('E', 4), ('F', 50), ('G', 6)])

        """
        if type(key) is slice:
            start, stop, step = self._unpack_slice(key)
            labels = itertools.islice(self.keys(), start, stop, step)

            if not isinstance(value, Iterable):
                value = [value]

            if len(value) == 1:
                value = itertools.cycle(value)
            else:
                labels, value = map(list, (labels, value))
                if len(labels) != len(value):
                    raise ValueError(
                        'Different argument lengths: keys ({}), values ({})'.format(
                            len(labels), len(value)))

            for k, v in zip(labels, value):
                super().__setitem__(k, v)
        else:
            super().__setitem__(key, value)
