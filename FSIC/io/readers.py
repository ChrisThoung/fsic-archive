# -*- coding: utf-8 -*-
"""
readers
=======
FSIC module to define individual file readers.

"""


import pandas as pd

from FSIC.settings import DTYPE


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
        'csvy': ',',
        'ycsv': ',',
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
        dtype=DTYPE)

def read_csvy(path, filetype, index_col='index', with_meta=False):
    """Return the contents of the delimiter-separated file with YAML header in `path`.

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
    with_meta : boolean
        If `True`, also return the YAML frontmatter as a Dictionary. Requires a
        YAML parser
        (see below for further details, under 'Returns' and 'Notes')

    Returns
    =======
    If `with_meta` is `False`:
        data : pandas DataFrame
            Contents of `path`

    If `with_meta` is `True`: two-element tuple with contents as follows:
        data : pandas DataFrame
            Data table in `path`
        meta : Dictionary
            Metadata in `path`, from the YAML frontmatter

    Notes
    =====
    If there is no YAML frontmatter at the beginning of this file (the first
    line is not '---'), this function behaves as if it were a regular CSV
    parser.

    This function requires a YAML parser to return the processed
    frontmatter. The function will raise an error if none of the supported
    parsers are available:

    * PyYAML: http://pyyaml.org/wiki/PyYAML

    For further information on the use of YAML frontmatter to store metadata, see:
        http://blog.datacite.org/using-yaml-frontmatter-with-csv/
        http://csvy.org/

    """
    frontmatter = None
    with open(path, 'rt') as f:
        first_line = f.readline().rstrip()
        if first_line == '---':
            frontmatter = []
            for line in f:
                line = line.rstrip()
                if line == '---':
                    break
                frontmatter.append(line)
            frontmatter = '\n'.join(frontmatter)
        else:
            f.seek(0)
        data = read_csv(f, filetype, index_col)
    if with_meta:
        try:
            import yaml
            frontmatter = yaml.load(frontmatter)
        except:
            raise ImportError
        return data, frontmatter
    else:
        return data

read_ycsv = read_csvy


functions = {
    'csv': {'function': read_csv, 'can_decompress': True},
    'csvy': {'function': read_csvy, 'can_decompress': False},
    'ycsv': {'function': read_ycsv, 'can_decompress': False},
    'tsv': {'function': read_csv, 'can_decompress': True},
}
