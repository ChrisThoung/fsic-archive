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

def wrap_lines(lines, line_length=80, word_sep=' ', line_sep='\n', strip_whitespace=True):
    """Wrap the contents of `lines` to be `line_length` characters long.

    Parameters
    ==========
    lines : string
        Text to wrap
    line_length : integer
        Maximum number of characters per line
    word_sep : string
        Word separator. Where possible, this function will attempt to preserve
        words by wrapping at instances of this string
    line_sep : string
        Line separator to identify individual lines in `lines` and to join the
        newly-wrapped lines back together
    strip_whitespace : logical
        If True, strip leading and trailing whitespace from the newly-wrapped
        lines

    Returns
    =======
    wrapped : string
        Version of `lines`, wrapped to a maximum of `line_length`

    Notes
    =====
    Where `word_sep` is not an empty string, this function attempts to split at
    word boundaries while still having each line have a maximum character length
    of `line_length`.

    Where this is not possible, the line is simply wrapped at `line_length`
    characters.

    """
    # Just return if wrapping not required
    if len(lines) <= line_length:
        return lines
    # Split by `line_sep`
    lines = lines.split(line_sep)
    # Wrap one line at a time
    wrapped = []
    for line in lines:
        while len(line) > line_length:
            rightmost_word_sep = line[:line_length + 1].rfind(word_sep)
            # Just set to `line_length` if no word separator found
            if rightmost_word_sep == -1:
                rightmost_word_sep = line_length
            wrapped.append(line[:rightmost_word_sep])
            line = line[rightmost_word_sep:]
        wrapped.append(line)
    # Strip whitespace
    if strip_whitespace:
        wrapped = [w.strip() for w in wrapped]
    # Join and return
    wrapped = line_sep.join(wrapped)
    return wrapped
