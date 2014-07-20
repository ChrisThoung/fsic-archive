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
    This function is to translates more basic Python expressions (e.g. from a
    Pandoc Markdown file) into ones that can be included in a Python class
    definition (i.e. a model class object). This consists of:

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
    # Remove unnecessary whitespace
    while('  ' in block):
        block = block.replace('  ', ' ')
    split_pattern = re.compile(
        r'''\b              # Open word boundary
            ([A-z_]+[\w]*)  # Valid Python identifier (starts with a letter or
                            # underscore, then any sequence of alphanumeric
                            # characters)
            \b              # Close word boundary
            \s              # Single whitespace character (having already
                            # removed all double instances)
            \[              # Open square (index) bracket
        ''',
        re.VERBOSE)
    block = split_pattern.sub(r'\1' + '[', block)
    # Prefix pattern to add 'self.'
    prefix_pattern = re.compile(
        r'''(               # New group
            \b              # Open word boundary
            [A-z_]+[\w]*    # Valid Python identifier
            \b              # Close word boundary
            )               # Close group
        ''',
        re.VERBOSE)
    block = prefix_pattern.sub('self.' + r'\1', block)
    # Index pattern for variables without a period index
    index_pattern = re.compile(
        r'''(                   # New group
            \b                  # Open word boundary
            self\.[A-z_]+[\w]*  # Valid Python identifier preceded by 'self.'
            \b                  # Close word boundary
            )                   # Close group
            [^[]                # Next character is *not* an opening square
                                # bracket
        ''',
        re.VERBOSE)
    block = index_pattern.sub(r'\1'.strip() + '[' + period + '] ', block)
    block = block.strip()
    # Index pattern for the last variable in each expression
    index_pattern_last = re.compile(
        r'''(                   # New group
            \b                  # Open word boundary
            self\.[A-z_]+[\w]*  # Valid Python identifier preceded by 'self.'
            $                   # End of string
            )                   # Close group
        ''',
        re.VERBOSE)
    block = index_pattern_last.sub(r'\1'.strip() + '[' + period + '] ', block)
    block = block.strip()
    # Insert pattern for variables with a lead/lag offset
    lead_lag_pattern = re.compile(
        r'''\[      # Open square (index) bracket
            \s*     # Any whitespace before
            (       # Open group
            [\d+-]+ # One or more digits, + or -
            )       # Close group
            \s*     # Any whitespace after
            \]      # Close square (index) bracket
        ''',
        re.VERBOSE)
    block = lead_lag_pattern.sub('[' + period + r'\1' + ']', block)
    # Return
    return block
