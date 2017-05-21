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
        values : iterable, default `None`
        index : iterable, defaults to [0, 1, ...]

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
