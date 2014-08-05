# -*- coding: utf-8 -*-
"""
string
======
FSIC utility functions to operate on strings.

"""


def indent(block, num_tabs=1, include_first_line=False, spaces_instead_of_tabs=True, spaces_to_tabs=4):
    """Return the code block in `block` with indents.

    Parameters
    ==========
    block : string
        Python code block to indent
    num_tabs : integer
        Number of tabs to indent
    include_first_line : logical
        Whether to also indent the first line
    spaces_instead_of_tabs : logical
        Whether to replace tabs with spaces
    spaces_to_tabs : integer
        If replacing tabs with spaces, how many spaces to use

    Returns
    =======
    indented : string
        Indented version of `block`

    """
    # Split lines and re-assemble with tabs as indents
    indented = block.splitlines()
    indentation = '\t' * num_tabs
    indented = ('\n' + indentation).join(indented)
    # If required, indent the first line
    if include_first_line:
        indented = indentation + indented
    # If required, replace tabs with spaces
    if spaces_instead_of_tabs:
        indented = indented.replace('\t', ' ' * spaces_to_tabs)
    # Return
    return indented
