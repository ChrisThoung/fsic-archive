# -*- coding: utf-8 -*-
"""
readers
=======
FSIC module to define individual file readers.

"""


import pandas as pd

from FSIC.settings import dtype


def read_csv(path, filetype, index_col='index'):
    """Return the contents of the delimiter-separated file in `path`.

    Parameters
    ==========
    path : string
        Location of file to read
    filetype : dictionary
        Further information on how to read the file in `path`, comprising a
        dictionary containing 'format' as a key, to indicate the format of the
        file.
        May also contain 'compression' as a key, to indicate the compression
        format of the file, if applicable.
    index_col : string
        The column to use as the index of the final DataFrame

    Returns
    =======
    data : pandas DataFrame
        Contents of `path`

    """
    delimiters = {
        'csv': ',',
        'tsv': '\t',
    }
    # Identify separator
    sep = delimiters[filetype['format']]
    # Identify compression type
    if 'compression' in filetype:
        compression = filetype['compression']
    else:
        compression = None
    # Read and return
    return pd.read_csv(
        path,
        sep=sep,
        compression=compression,
        index_col=index_col,
        dtype=dtype)


functions = {
    'csv': {'function': read_csv, 'can_decompress': True},
    'tsv': {'function': read_csv, 'can_decompress': True},
}
