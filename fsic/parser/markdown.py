# -*- coding: utf-8 -*-
"""
markdown
========
FSIC parser to operate on Pandoc Markdown-formatted strings, in order to
extract code chunks.

"""


import re


def extract(script):
    """Return the code chunks from `script`.

    Parameters
    ==========
    script : string
        Pandoc Markdown-formatted text

    Returns
    =======
    chunks : list of strings
        One string per chunk

    """
    pattern = re.compile(
        r'''^[~`]{3,}   # Chunk begins with at least three tildes or backticks
                        # at the start of a line
            \{.+?\}\n   # Immediately followed by attributes, in braces (non-greedy)
            .*?         # Non-greedy quantifier (guards against blocks not separated
                        # by a double newline)
            ^[~`]{3,}$  # Chunk ends with at least three tildes or backticks
                        # at the start of a line
        ''',
    re.DOTALL | re.MULTILINE | re.VERBOSE)
    split = pattern.findall(script)
    return split
