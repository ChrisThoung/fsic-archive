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


# Valid file extensions
valid_filetypes = [
    'csv',
    'tsv',
]


def read(path, filetype=None, fail_on_error=True):
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
    fail_on_error : boolean
        If `True`, raise a runtime error in the event of a failed read
        operation. If `False`, continue

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
    2. If `path` is a zip archive, open the archive and loop through its
       contents, calling this function again to read the archived data

    Otherwise:

    3. Match the filetype to the relevant function in `FSIC.io.readers`
    4. Call the relevant function and return its return value

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
    # 2. If `path` is a zip archive, open the archive and loop through its
    #    contents, calling this function again to read the archived data
    if 'compression' in filetype and filetype['compression'] == 'zip':
        pass
    # 3. Match the filetype to the relevant function in `FSIC.io.readers`
    # 4. Call the relevant function and return its return value


def detect_filetype(path, compressed_types=['gz'], archive_types=['zip']):
    """Return the file extension(s) in `path` as a dictionary.

    Parameters
    ==========
    path : string
        The input filepath to process
    compressed_types : list of strings
    archive_types : list of strings
        File extensions that denote archives of files, for which a further
        file-format extension is not necessary

    Returns
    =======
    filetype : either:
               - a dictionary, if a filetype was successfully detected
               - None, if a filetype was not successfully detected
        If a dictionary, `filetype` will contain one or more of the following
        keys:
        - 'format' : the file extension that signifies the format of the data
                     in `path`
        - 'compression' : if compressed, the compression type of the file

    Notes
    =====
    A valid filepath must have at least one file extension. In the case of just
    one file extension, the file extension is assumed to denote the format of
    the data file e.g. 'csv', 'tsv', 'zip' archive.

    Note that the contents of the return dictionary differ depending on whether
    the extension is listed in `archive_types` (in which case, it is stored with
    key 'compression') or not (stored with key 'format').

    A valid filepath can have at most two file extensions (any that precede the
    last two are ignored). In this case:

    * The last (rightmost) file extension must denote the compression type
      i.e. be listed in `compressed_types`; it is stored with key 'compression'
    * The penultimate extension denotes the format of the data, stored with key
      'format'

    """
    # Attempt to extract last two file extensions
    stub1, ext1 = os.path.splitext(path)
    stub2, ext2 = os.path.splitext(stub1)
    # Clean file extensions
    ext1 = clean_file_ext(ext1)
    ext2 = clean_file_ext(ext2)
    # Initialise dictionary to store final return values
    filetype = {}
    # Check for compressed/archived file extension and, if found, either:
    # - Return, if the compressed format is in `archive_types`
    # - Re-assign `ext1` to be `ext2` i.e. the extension of the file in its
    #   uncompressed form
    if ext1 in compressed_types + archive_types:
        filetype['compression'] = ext1
        if ext1 in archive_types:
            return filetype
        ext1 = ext2
    # Return `None` if length of `ext1` is zero
    if len(ext1) == 0:
        return None
    # Assign format and return
    filetype['format'] = ext1
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
