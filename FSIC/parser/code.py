# -*- coding: utf-8 -*-
"""
code
====
FSIC parser to operate on Python code blocks extracted from code chunks, in
order to generate class definition-compatible code.

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
            (?!\()          # Next character is *not* an opening bracket
                            # (necessary to ignore function calls)
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
            (?!\[)              # Next character is *not* an opening square
                                # bracket
        ''',
        re.VERBOSE)
    block = index_pattern.sub(r'\1'.strip() + '[' + period + ']', block)
    block = block.replace('[' + period + ']]', ']')
    # Insert patterns for variables with lead/lag offsets
    lead_pattern = re.compile(
        r'''\[      # Open square (index) bracket
            \s*     # Any whitespace before
            (       # Open group
            [\d]+   # One or more digits (no sign)
            )       # Close group
            \s*     # Any whitespace after
            \]      # Close square (index) bracket
        ''',
        re.VERBOSE)
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
    block = lead_pattern.sub('[' + period + '+' + r'\1' + ']', block)
    block = lead_lag_pattern.sub('[' + period + r'\1' + ']', block)
    # Return
    return block


def identify_variables(statement, prefix=r'self\.', suffix=r'', remove_duplicates=True, sort_variables=True):
    """Identify the endogenous and exogenous variables in `statement`.

    Parameters
    ==========
    statement : string
        Python code block to parse
    prefix : string
        String each variable should begin with, to be included in the search
        regular expression (use `r'\b'` if no prefix desired)
    suffix : string
        String each variable should end with, to be included in the search
        regular expression (use `r'\[.+?\]'` to preserve trailing time index)
    remove_duplicates : logical
        If True, remove duplicate entries. Where a variable appears as both
        an endogenous and an exogenous variable, retain the variable as an
        endogenous variable
    sort_variables : logical
        If True, sort the variables alphabetically before returning

    Returns
    =======
    variables : Dictionary
        Contains:
            'endogenous' : list of strings
                Names of endogenous variables (to the left of the equals sign)
            'exogenous' : list of strings
                Names of exogenous variables (to the right of the equals sign)

    Examples
    ========
    >>> import fsic.parser.code.identify_variables as identify_variables
    >>> identify_variables('self.C_s[0] = self.C_d[0]')
    {'endogenous': ['C_s'],
     'exogenous': ['C_d']})

    >>> import fsic.parser.code.identify_variables as identify_variables
    >>> identify_variables('C_s[0] = C_d[0]', prefix=r'\b')
    {'endogenous': ['C_s'],
     'exogenous': ['C_d']})

    """
    pattern = re.compile(
        prefix +
        r'''(?<!\[)     # Preceding character is *not* an opening square bracket
            \b          # Word boundary
            [A-Za-z_]+  # Valid Python identifier opening character(s)
            \w*         # Any other characters in a valid Python identifier
        ''' +
        suffix,
        re.VERBOSE)
    # Split lines and then parse line by line
    statement = statement.splitlines()
    endogenous = []
    exogenous = []
    for l in statement:
        # Split by equals sign and then parse
        n, x = l.split('=', 1)
        endogenous = endogenous + list(pattern.findall(n))
        exogenous = exogenous + list(pattern.findall(x))
    # Check for duplicates, if required
    if remove_duplicates:
        # Remove duplicates from individual lists
        endogenous = list(set(endogenous))
        exogenous = list(set(exogenous))
        # Find the union of the two sets and remove from `exogenous`
        union = list(set(endogenous) & set(exogenous))
        exogenous = [x for x in exogenous if x not in union]
    # Sort alphabetically
    if sort_variables:
        endogenous = list(sorted(endogenous))
        exogenous = list(sorted(exogenous))
    # Store to Dictionary and return
    variables = {
        'endogenous': list(endogenous),
        'exogenous': list(exogenous), }
    return variables
