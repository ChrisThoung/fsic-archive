# -*- coding: utf-8 -*-
"""
csvy
====
FSIC I/O module for files with CSV data, possibly with YAML frontmatter. Wraps
`pandas` `read_csv()` function.

"""

import pandas as pd
import yaml


def read_csvy(filepath_or_buffer, return_frontmatter=False, *args, **kwargs):
    """Wrapper for `pandas.read_csv()`, to allow for YAML frontmatter.

    Parameters
    ----------
    filepath_or_buffer : as for `pandas` `read_csv()`
    return_frontmatter : boolean, default `False`
        Return YAML frontmatter alongside the data, as a 2-tuple
    args, kwargs : further arguments for `pandas` `read_csv()`

    Returns
    -------
    df : `DataFrame`
    fm : `dict`, in a 2-tuple, (`df`, `tm`), if `return_frontmatter` is `True`

    """
    if isinstance(filepath_or_buffer, str):
        filepath_or_buffer = open(filepath_or_buffer, 'r')

    fm = None
    # If found, parse YAML frontmatter...
    if filepath_or_buffer.readline().rstrip() == '---':
        fm = []
        for line in filepath_or_buffer:
            if line.rstrip() == '---':
                break
            fm.append(line)
        fm = yaml.load('\n'.join(fm))
    # ...otherwise, return to start of file
    else:
        filepath_or_buffer.seek(0)

    df = pd.read_csv(filepath_or_buffer, *args, **kwargs)
    filepath_or_buffer.close()

    if return_frontmatter:
        return df, fm
    else:
        return df
