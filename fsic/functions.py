# -*- coding: utf-8 -*-
"""
functions
=========
Functions to transform data and create vectors and matrices (as `pandas`
`Series` and `DataFrame` objects, respectively).

"""

import numpy as np

from pandas import Series, DataFrame
import pandas as pd


def lag(x, p=1):
    return x.shift(p)

def diff(x, d=1):
    return x - lag(x, d)

def dlag(x, p=1, d=1):
    return lag(diff(x, d), p)

def dlog(x, d=1):
    return diff(np.log(x), d)


def time_trend(index, *, loc=None, iloc=None, key=None, value=0, descending=False):
    """Create a time trend from `index`, as a `Series` object.

    Parameters
    ----------
    index : iterable
        Index for the return variable
    iloc : int (location in `index`), default `None`
    loc : item in `index`, default `None`
        User can optionally set one of `iloc` or `loc` (but **not
        both**). Follows a similar logic to the indexing methods in `pandas`:
         - `iloc` : integer position of the item in `index` to use as the
                    centre of the time trend
         - `loc` : item in `index` to use as the centre of the time trend
    key : one-argument function, default `None`
        If `loc` is not `None`, use `key()` to locate `loc` in `index`. If
        `key` is `None`, try `index.get_loc()` (`pandas` method) and then
        `index.index()` (Python `list`/`tuple` method). Raise an
        `AttributeError` on failure
    value : numeric, default 0
        Numeric value to use at the centre of the time trend
    descending : bool, default `False`
        If `True`, return a descending, rather than an ascending, time trend

    Returns
    -------
    : `pandas` `Series`

    """
    if iloc is not None and loc is not None:
        raise ValueError('Can only set one of `iloc` and `loc`')

    if iloc is None and loc is None:
        # Default case if no modifying arguments
        centre = 0
    elif iloc is not None:
        centre = iloc
        # Adjust for negative indexing
        if centre < 0:
            centre += len(index)
    elif loc is not None:
        if key is None:
            if hasattr(index, 'get_loc'):
                centre = index.get_loc(loc)
            elif hasattr(index, 'index'):
                centre = index.index(loc)
            else:
                raise AttributeError('Unable to find a default indexing method')
        else:
            centre = key(loc)

    if descending:
        start = value + centre
        end = start - len(index) + 1
        offset = increment = -1
    else:
        start = value - centre
        end = start + len(index) - 1
        offset = increment = 1

    return Series(range(start, end + offset, increment), index=index)


indicator_types = ('impulse', 'step', 'trend', 'plateau', )

def indicator_matrix(index, *, kind, drop_constants=False, **kwargs):
    """Create a matrix of indicators, as a `DataFrame` object.

    Parameters
    ----------
    index : iterable
        Index for the return variable; also the basis for the column names
    kind : str {'impulse', 'step', 'trend', 'plateau'}
        The type of indicator to create
    drop_constants : bool, default `False`
        If `True`, drop columns of constant terms. Only affects the return
        value if `kind` is {'step', 'trend', 'plateau'}
    **kwargs : keyword arguments to pass to other functions, as necessary

    Returns
    -------
    indicators : `pandas` `DataFrame`

    """
    if kind not in indicator_types:
        raise ValueError('Invalid `kind` argument: {}'.format(kind))

    T = len(index)

    if kind == 'impulse':
        matrix = np.identity(T)
        prefix = 'I'
    elif kind == 'step':
        matrix = np.tril(np.ones([T, T]), 0)
        prefix = 'S'
    elif kind == 'trend':
        matrix = pd.concat([time_trend(index, **kwargs).shift(i).fillna(0)
                            for i in range(T)], axis=1).values
        prefix = 'T'
    elif kind == 'plateau':
        matrix = pd.concat([t.fillna(t.max())
                            for t in [time_trend(index, **kwargs).shift(-i)
                                      for i in range(T)]], axis=1).values
        prefix = 'P'

    indicators = DataFrame(matrix,
                           index=index,
                           columns=['{}{}'.format(prefix, i) for i in index])
    if drop_constants:
        constant_terms = [name
                          for name, column in indicators.iteritems()
                          if len(column.unique()) == 1]
        if len(constant_terms):
            indicators = indicators.drop(constant_terms, axis=1)

    return indicators
