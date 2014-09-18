# -*- coding: utf-8 -*-
"""
read
====
FSIC module to handle data input for models. By default, uses the file extension
of a path to process an input file, returning a pandas DataFrame.

"""


import os
from pandas import Series, DataFrame
import pandas as pd


# Valid file extensions
valid_filetypes = [
    'csv',
    'tsv',
]
valid_compressed_types = [
    'gz',
    'zip',
]


def read(path, filetype=None):
    """Return the contents of `path` as a pandas DataFrame.

    Parameters
    ==========
    path : string
        Path of input file to read
    filetype : string or `None`
        If `None`, the function will attempt to determine the filetype of the
        input file according to its file extension. Otherwise, `filetype` must
        be a string that specifies the file extension to use (the leading dot is
        optional)

    Returns
    =======
    data : pandas DataFrame
        Contents of `path`

    Notes
    =====
    This function acts as a wrapper around the individual functions to handle
    specific file types (in `FSIC.io.readers`).

    The steps are as follows:

    1. Identify the filetype, if not specified explicitly in `filetype`
    2. Match the filetype to the relevant function in `FSIC.io.readers`
    3. Call the relevant function and return its return value

    The vast majority of readers provide at least some support for compressed
    files:

    * gzip format (file extension: 'gz') for individual files is handled as an
      additional file extension e.g. 'tsv' compared to 'tsv.gz' - the 'gz'
      extension is interpreted as requiring decompression first before passing
      the contents to the regular TSV file parser. The same would hold for 'csv'
      etc

    * zip archives (file extension: 'zip') are more complicated, as they contain
      multiple files. By default, these are handled as follows:
        *

    """
    # 1. Identify the filetype, if not specified explicitly in `filetype`
    if filetype is None:
        filetype = detect_filetype(path)
    else:
        filetype = clean_filetype(filetype)
    # 2. Match the filetype to the relevant function in `FSIC.io.readers`
    # 3. Call the relevant function and return its return value


def detect_filetype(path, sep='.'):
    """Return the cleaned file extension(s) in `path`.

    Parameters
    ==========
    path : string
        The input filepath to process
    sep : string
        String to split file extensions

    Returns
    =======
    filetype : string
        The file extension(s) identified from `path`

    """
    # Raise error if `sep` not found (nothing to separate by)
    if sep not in path:
        raise ValueError(
            'Unable to split `path`: no instances of `sep` (\'%s\') found' %
            sep)
    # Split by `sep`
    pieces = path.split(sep)
    # Extract last piece
    file_ext = pieces.pop(-1)
    if file_ext in valid_compressed_types:
        file_ext, compressed_ext = pieces.pop(-1), file_ext
    if file_ext not in valid_filetypes:
        raise ValueError(
            'Unable to identify a valid file extension in `path`: %s' %
            path)
    return


def clean_filetype(filetype):
    pass
