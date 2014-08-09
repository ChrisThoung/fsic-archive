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

def wrap_text(text, num_chars=80, delim=' ', sep='\n'):
    """Wrap `text` to `num_chars` characters per line.

    Parameters
    ==========
    text : string
        Text to wrap
    num_chars : integer
        Number of characters per line
    delim : string
        String to define word boundaries
    sep : string
        String to separate lines with

    Returns
    =======
    wrapped : string
        Copy of `text`, wrapped to `num_chars` characters using `sep`

    """
    # No change if already less than num_chars
    if len(text) <= num_chars:
        return text
    # Split by `sep`
    lines = text.split(sep)
    # Wrap one line at a time
    wrapped = []
    for line in lines:
        if len(line) > num_chars:
            while len(line) > num_chars:
                last_delim = line[:num_chars+1].rfind(delim)
                if last_delim == -1:
                    last_delim = num_chars
                wrapped.append(line[:last_delim])
                line = line[last_delim:]
        wrapped.append(line)
    # Join and return
    wrapped = [w.strip() for w in wrapped]
    wrapped = sep.join(wrapped)
    return wrapped
