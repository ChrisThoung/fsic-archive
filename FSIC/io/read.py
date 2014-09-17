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


def detect_filetype(path, max_exts=2, sep='.'):
    """Return the cleaned file extension(s) of `path`.

    Parameters
    ==========
    path : string
        The input filepath to process
    max_exts : integer
        The maximum number of extensions to extract from `path` e.g. to handle
        extensions such as 'tsv.gz' or 'csv.zip'
    sep : string
        String to split file extensions

    Returns
    =======
    filetype : string
        The file extension(s) identified from `path`

    """
    # Split into individual pieces
    pieces = path.split(sep)
    # Search back from the end for valid filetypes to locate the first valid
    # extension
    found = False
    for first_ext, p in enumerate(reversed(pieces)):
        if p in valid_filetypes or p in valid_compressed_types:
            found = True
        else:
            break
    # Raise an error if no valid file extensions found
    if not found:
        raise ValueError('No valid file extensions found in: %s' % path)
    # Extract valid extensions only and join back together
    exts = pieces[-min(first_ext, max_exts):]
    exts = sep.join(exts)
    # Return
    return exts


def clean_filetype(filetype):
    pass
