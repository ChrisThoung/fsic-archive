# -*- coding: utf-8 -*-
"""
utilities
=========
Generic FSIC utility functions.

"""

from pandas import DataFrame
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
                    merged.ix[row, column] = comparison_functions[column](
                        new_value, merged.ix[row, column])
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
        if ((a in exclusive and a != b) or
            (b in exclusive and a != b)):
            raise SpecificationError
        selected = min(precedence.index(a), precedence.index(b))
        return precedence[selected]

    return compare
