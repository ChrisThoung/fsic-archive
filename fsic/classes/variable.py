# -*- coding: utf-8 -*-
"""
variable
========
Container based on standard-library `OrderedDict` class, augmented with
`pandas`-style indexing (aping the behaviour of the `Series` class).

"""

from collections import OrderedDict
import itertools


class Variable(OrderedDict):
    """`OrderedDict`-based container with `pandas` Series-style indexing."""

    def __init__(self, values, index=None):
        """Initialise object with values and index (keys).

        Parameters
        ----------
        values : constant (*requires* an `index` argument) or iterable
        index : iterable; default: `range(0, len(values))`

        """

        if index is None:
            # No index: (infinite) counter to implement a `range`-like
            index = itertools.count()
        elif not hasattr(values, '__iter__') or isinstance(values, str):
            # Constant: (infinite) cycler over length of `index`
            values = itertools.cycle([values])

        super().update(zip(index, values))
