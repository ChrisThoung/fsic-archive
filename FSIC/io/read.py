# -*- coding: utf-8 -*-
"""
read
====
FSIC module to handle data input for models. By default, uses the file extension
of a path to process an input file, returning a pandas DataFrame.

"""


import os
import zip

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
    data : list of pandas DataFrame objects
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
        * Identify all files in the archive that are themselves valid as data
          files. Files in the archive can also be compressed (creating the
          potential for a tree of compressed files)
        * Loop through the file list and extract

    """
    # 1. Identify the filetype, if not specified explicitly in `filetype`
    if filetype is None:
        filetype = detect_filetype(path)
    else:
        filetype = clean_filetype(filetype)
    # 2. Match the filetype to the relevant function in `FSIC.io.readers`
    # 3. Call the relevant function and return its return value


def detect_filetype(path):
    """Return the file extension(s) in `path` as a dictionary.

    Parameters
    ==========
    path : string
        The input filepath to process

    Returns
    =======
    filetype : dictionary
        The file extension(s) identified in `path`, with keys as follows:
        'format' : the file extension that signifies the format of the data in
                   `path`
        'compression' : the file extension/format of the compressed file, if
                        applicable ('' if none found)

    Notes
    =====
    A valid filepath must satisfy one of the following:

    1. End with one file extension that describes the format of the data
    2. End with two file extensions, the first (leftmost/penultimate) one
       describing the format of the data; the second (rightmost/last) indicating
       the compression type

    """
    # Attempt to extract last two file extensions
    stub1, ext1 = os.path.splitext(path)
    stub2, ext2 = os.path.splitext(stub1)
    # Clean file extensions
    ext1 = clean_file_ext(ext1)
    ext2 = clean_file_ext(ext2)
    # Initialise dictionary to store final return values
    filetype = {}
    # Check for compressed file extension and re-assign `ext1` as required
    if ext1 in valid_compressed_types:
        filetype['compression'] = ext1
        ext1 = ext2
    else:
        filetype['compression'] = ''
    # Check for valid filetype
    if ext1 not in valid_filetypes:
        raise ValueError('Unable to locate file extension in: %s' % path)
    # Assign
    filetype['format'] = ext1
    # Return
    return filetype


def clean_file_ext(ext):
    """Return `ext` without the leading dot, if found.

    Parameters
    ==========
    ext : string
        File extension to clean

    Returns
    =======
    ext : string
        Modified version of `ext`

    """
    if ext.startswith('.'):
        ext = ext[1:]
    return ext
