# -*- coding: utf-8 -*-
"""
api
===
FSIC data I/O API.

"""

import os

import numpy as np

from pandas import DataFrame
import pandas as pd

from FSIC.exceptions import FSICError
from FSIC.io.csvy import read_csvy, write_csvy


readers = {
    '.csv': read_csvy,
    '.csvy': read_csvy,
}


def read(files, *args, fill=np.nan, **kwargs):
    """Return the contents of `files` as a single `pandas` `DataFrame`.

    Parameters
    ----------
    files : str or iterable of str
        Input filepath(s) to read
    fill : numeric
        Fill value
    *args, **kwargs : as for underlying file readers
        Additional arguments to pass to file-specific read functions

    Returns
    -------
    data : `pandas` `DataFrame`
        Consolidated data

    """
    if type(files) is str:
        files = [files]
    elif not hasattr(files, '__iter__'):
        raise ValueError(
            '`files` is neither a string nor an iterable of strings')

    # Collect input data
    frames = []
    for path in files:
        ext = os.path.splitext(path)[1]

        try:
            function = readers[ext]
        except KeyError:
            raise FSICError(
                "No reader implemented for file extension: '{}'".format(ext))

        frames.append(function(path, *args, **kwargs))

    # Combine into a single DataFrame
    data = None
    for f in frames:
        if data is None:
            data = f.copy()
        else:
            union = DataFrame(fill,
                              index=data.index.union(f.index),
                              columns=data.columns.union(f.columns))
            union.loc[data.index, data.columns] = data
            union.loc[f.index, f.columns] = f
            data = union.copy()

    return data
