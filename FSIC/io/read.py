# -*- coding: utf-8 -*-
"""
read
====

FSIC module to handle data input for models. By default, uses the file
extension of a path to process an input file, returning a pandas DataFrame.

"""


import os
import tempfile
import zipfile

from FSIC.io.readers import functions as readers


archive_extensions = ['zip']


def read(path, method=None, fail_on_error=True):
    """Return the contents of `path` as a list of pandas DataFrame objects.

    Parameters
    ==========
    path : string
        Location of file to read
    method : `None` or string
        If `None`, attempt to detect the format of the file in `path` based on
        its file extension(s).
        If a string, this variable specifies the file extensions to use for
        reading.
    fail_on_error : boolean
        If `True`, raise a `ValueError` in the event that the filetype cannot
        be identified. If False, return `None`

    Returns
    =======
    data : list of pandas DataFrames
        Contents of the file in `path`

    """
    # If method is `None`, attempt to identify the type of the file in `path`
    if method is None:
        method = filetype(path)
        if method is None:
            if fail_on_error:
                raise ValueError(
                    'Unable to identify valid file extension(s) in: %s' % path)
            else:
                return None
    else:
        method = {'format': clean_file_ext(method)}
    # If method contains an archive file extension, loop through and call this
    # function again
    if 'compression' in method and method['compression'] in archive_extensions:
        compression = method['compression']
        if compression == 'zip':
            data = []
            with zipfile.ZipFile(path, 'r') as z:
                for n in z.namelist():
                    with tempfile.NamedTemporaryFile(delete=False) as t:
                        t.write(z.open(n).read())
                        t.flush()
                        temp_path = t.name
                    data.append(
                        read(
                            temp_path,
                            method=filetype(n)['format'],
                            fail_on_error=False)[0])
                    try:
                        os.remove(temp_path)
                    except:
                        pass
        else:
            raise ValueError(
                'Currently no method to deal with archive format: %s' %
                compression)
    # Otherwise, identify the relevant `reader` function, read `path` and
    # return its contents as a one-element list
    else:
        #
        reader = readers[method['format']]
        read_function = reader['function']
        can_decompress = reader['can_decompress']
        if 'compression' not in method or can_decompress:
            data = read_function(path, method)
            data = [data]
        else:
            raise ValueError('Unable to decompress file in: %s' % path)
    # Return
    return data


def filetype(path, compressed_exts=['gz'], archive_exts=archive_extensions):
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
