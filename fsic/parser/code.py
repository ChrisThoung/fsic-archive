# -*- coding: utf-8 -*-
"""
code
====
FSIC parser to generate model-compatible Python code from code blocks.

"""


import re


def translate(block, period='period'):
    """Convert the code in `block` to a model-compatible code block.

    Parameters
    ==========
    block : string
        Code block to translate
    period : string
        Name to use as the period index

    Returns
    =======
    block : string
        Translated code

    Notes
    =====
    The purpose of this function is to translate more basic Python expressions
    (e.g. from a Pandoc Markdown file) into ones that can be included in a
    Python class definition (i.e. a model class object). This consists of:

    * Adding 'self.' as a prefix
    * Adding a period index as a suffix (accounting for leads and lags where
      appropriate)

    Examples
    ========
    >>> import fsic.parser.code.translate as translate
    >>> translate('C_s = C_d')
    'self.C_s[period] = self.C_d[period]'

    >>> import fsic.parser.code.translate as translate
    >>> translate('G_s = G_d', period='time')
    'self.G_s[time] = self.G_d[time]'

    """
    pattern = re.compile(
        r'''(               # New group
            \b              # Open word boundary
            [A-z_]+[\w]*    # Valid Python identifier (starts with a letter or
                            # underscore, then any sequence of alphanumeric
                            #  characters)
            \b              # Close word boundary
            )               # Close group
        ''',
        re.VERBOSE)
    block = pattern.sub('self.' + r'\1'+ '[' + period + ']', block)
    return block
