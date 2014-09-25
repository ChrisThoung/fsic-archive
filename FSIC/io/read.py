# -*- coding: utf-8 -*-
"""
read
====
FSIC module to handle data input for models. By default, uses the file extension
of a path to process an input file, returning a pandas DataFrame.

"""


import os
import zipfile

from pandas import Series, DataFrame
import pandas as pd


def filetype(path, compressed_exts=['gz'], archive_exts=['zip']):
    """Return the filetypes of `path` as a dictionary.

    Parameters
    ==========
    path : string
    compressed_exts : list of strings
        File extensions that indicate individual compressed files
    archive_exts : list of strings
        File extensions that indicate (compressed) file archives

    Returns
    =======
    If filetypes not successfully identified: `None`

    Otherwise:
        types : dictionary
            Containing one or more of the following keys:
             - 'format' : string
               The extension indicating the format of the data in `path`
             - 'compression' : string
               The compression format of the file

    Examples
    ========
    >>> from FSIC.io.read import filetype
    >>> filetype('input.csv')
    {'format': 'csv'}

    >>> filetype('input.csv.gz')
    {'format': 'csv', 'compression': 'gz'}

    >>> filetype('input.zip')
    {'compression': 'zip'}

    >>> filetype('this_file_has_no_extension')
    None

    """
    # Extract filename from filepath
    path = os.path.split(path)[1]
    # Form dictionary to return
    types = {}
    while True:
        # Split out file extension and clean
        path, ext = os.path.splitext(path)
        ext = clean_file_ext(ext)
        # If file is compressed, store extension and loop again...
        if ext in compressed_exts:
            types['compression'] = ext
        # ...otherwise, process extension and break
        else:
            # No file extension found: Set to `types` to `None`
            if len(ext) == 0:
                types = None
            # File is an archive: Store archive extension only
            elif ext in archive_exts:
                types['compression'] = ext
            # Extension found: Store
            else:
                types['format'] = ext
            break
    # Return
    return types


def clean_file_ext(ext):
    """Return `ext`, dropping the leading dot, if present.

    Parameters
    ==========
    ext : string
        File extension to clean

    Returns
    =======
    ext : string
        Clean version of `ext`

    """
    if ext.startswith('.'):
        ext = ext[1:]
    return ext
