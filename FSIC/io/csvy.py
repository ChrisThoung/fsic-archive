# -*- coding: utf-8 -*-
"""
csvy
====
FSIC I/O module for files with CSV data, possibly with YAML
frontmatter. Provides wrappers for `pandas` `read_csv()` function and
`to_csv()` method.

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


def write_csvy(data, path_or_buf=None, frontmatter=None, *args, **kwargs):
    """Wrapper for `pandas` `to_csv()`, to allow for YAML frontmatter.

    Parameters
    ----------
    data : object to write (must have a `to_csv()` method)
    path_or_buf : as for object's `to_csv()` method, default `None`
        Destination for output
    frontmatter : other data to write, typically list- or dict-like,
                  default `None`
        Optional frontmatter to store as YAML
    args, kwargs : further arguments for object's `to_csv()` method

    Returns
    -------
    If `path_or_buf` is `None`: the result as a string

    """
    mode = kwargs.pop('mode', 'w')

    header = ''
    if frontmatter is not None:
        header = '''\
---
{}
---
'''.format(yaml.dump(frontmatter, default_flow_style=False).strip())

        if path_or_buf is not None:
            if hasattr(path_or_buf, 'write'):
                path_or_buf.write(header)
            else:
                with open(path_or_buf, mode) as f:
                    print(header, file=f, end='')

        mode = 'a'

    result = data.to_csv(path_or_buf, *args, mode=mode, **kwargs)

    if path_or_buf is None:
        return header + result
