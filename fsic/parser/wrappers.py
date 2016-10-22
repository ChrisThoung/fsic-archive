# -*- coding: utf-8 -*-
"""
wrappers
========
FSIC module to provide wrappers for Markdown parser.

"""

import os
from fsic.parser.markdown import read_markdown


wrapper_docstring = """Read the {language} model specification in `filepath_or_string`.

    Parameters
    ----------
    filepath_or_buffer : str
        {language} input to read. Can be either a path to the input file or a
        string of {language} code.

    Returns
    -------
    schematic : FSIC `Schematic` object
        The parsed model specification

    """


def read_python(filepath_or_string):
    if os.path.exists(filepath_or_string):
        filepath_or_string = open(filepath_or_string, 'r').read()
    return read_markdown('``` {#Python .python}\n' +
                         filepath_or_string +
                         '\n```')
read_python.__doc__ = wrapper_docstring.format(language='Python')
