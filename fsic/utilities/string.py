# -*- coding: utf-8 -*-
"""
string
======
FSIC utility functions to operate on strings.

"""


def indent_lines(block, num_tabs=1, expand_tabs=True, tab_size=4, skip_first_line=False):
    """Return `block` indented with additional tabs on each line.

    Parameters
    ==========
    block : string
        Block to indent after newlines
    num_tabs : integer
        Number of tabs to indent by
    expand_tabs : logical
        If True, convert tabs to spaces
    tab_size : integer
        If `expand_tabs` is True, `tab_size` sets the number of spaces
        per tab
    skip_first_line : logical
        If True, don't indent the first line

    Returns
    =======
    indented : string
        Indented version of `block`

    """
    indentation = '\t' * num_tabs
    # Split lines and reassemble with tabs for all but the first line
    indented = block.splitlines()
    indented = ('\n' + indentation).join(indented)
    # Indent the first line
    if not skip_first_line:
        indented = indentation + indented
    # Expand tabs
    if expand_tabs:
        indented = indented.expandtabs(tab_size)
    # Return
    return indented
