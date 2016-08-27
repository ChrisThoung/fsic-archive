# -*- coding: utf-8 -*-
"""
utilities
=========
Generic FSIC utility functions.

"""

import numpy as np

from pandas import Period
from pandas import Series, DataFrame
from pandas.tslib import DateParseError
import pandas as pd

from FSIC.exceptions import SpecificationError


def merge_frames(frames_to_merge, comparison_functions):
    """Merge the DataFrames in `frames_to_merge` according to the functions in `comparison_functions`.

    Parameters
    ----------
    frames_to_merge : list of DataFrames
        Objects to merge
    comparison_functions : dictionary
         - keys should match the columns in the individual items in
           `frames_to_merge`
         - values should be functions that take pairs of inputs and return the
           highest-priority one

    Returns
    -------
    merged : DataFrame
        Columns match those of the individual DataFrames, with values
        overwritten according to `comparison_functions`. The index (rows) is
        the union of the objects' indexes.

    """
    merged = None
    for df in frames_to_merge:
        if merged is None:
            merged = df.copy()
            continue
        for row, entry in zip(df.index, df.itertuples(index=False)):
            entry = dict(zip(df.columns, entry))
            if row in merged.index:
                for column, new_value in entry.items():
                    merged.loc[row, column] = comparison_functions[column](
                        new_value, merged.loc[row, column])
            else:
                merged = pd.concat([merged, DataFrame(entry, index=[row])])
    return merged

def merge_dicts(dicts_to_merge, comparison_functions):
    """Merge the items in `dicts_to_merge` according to the functions in `comparison_functions`.

    Parameters
    ----------
    dicts_to_merge : list of dict-likes
        Objects to merge
    comparison_functions : dictionary
         - keys should match those of the individual items in `dicts_to_merge`
         - values should be functions that take pairs of inputs and return the
           highest-priority one

    Returns
    -------
    merged : dict-like
        Object with keys matching those of the items in `dicts_to_merge`, with
        values overwritten according to `comparison_functions`

    """
    merged = None
    for d in dicts_to_merge:
        if merged is None:
            merged = d.copy()
            continue
        for k, new_value in d.items():
            merged[k] = comparison_functions[k](new_value, merged[k])
    return merged

def make_comparison_function(precedence, exclusive=None):
    """Make a function that returns the earliest entry in `precedence`.

    Parameters
    ----------
    precedence : list-like
        Terms to compare. Terms nearer the beginning are of higher precedence
    exclusive : list-like, default `None`
        If a list-like, throw a `SpecificationError` if a term is in
        `exclusive` but does not match the comparator term. This is because
        such terms should always be identical.

    """
    if exclusive is None:
        exclusive = ()

    def compare(a, b):
        if a in exclusive or b in exclusive:
            if a != b:
                raise SpecificationError
            else:
                return a
        selected = min(precedence.index(a), precedence.index(b))
        return precedence[selected]

    return compare


def locate_in_index(index, period) -> int:
    """Return the location of `period` in `index`.

    Parameters
    ----------
    index : `pandas` `Index`-like
        Array to search in (an object with a `get_loc()` method)
    period : int, str or valid argument to `pandas` `Period` class
        Item to search for

    Returns
    -------
    : int
        The location of `period` in `index`

    """
    if index.holds_integer():
        period = int(period)
    else:
        try:
            period = Period(period)
        except DateParseError:
            pass
    return index.get_loc(period)


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
