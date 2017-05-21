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
