# -*- coding: utf-8 -*-
"""
chunk
=====
FSIC parser to convert code chunks into Dictionary objects.

"""


import re


def split(chunk):
    """Split `chunk` into an attributes string and a code string.

    Parameters
    ==========
    chunk : string
        Code chunk to split

    Returns
    =======
    contents : Dictionary
        Contains:
            'attributes' : string
                Code-block attributes
            'code' : string
                The code itself

    """
    pattern = re.compile(
        r'''^[~`]{3,}                   # Chunk begins with at least three
                                        # tildes or backticks at the start
                                        # of a line
            \{(?P<attributes>.+?)\}\n   # Attributes inside braces
            (?P<code>.*?)               # Remainder is code
            ^[~`]{3,}$                  # Chunk ends with at least three
                                        # tildes or backticks at the start
                                        # of a line
        ''',
        re.DOTALL | re.MULTILINE | re.VERBOSE)
    m = pattern.search(chunk)
    contents = {
        'attributes': m.group('attributes').strip(),
        'code': m.group('code').strip()
        }
    return contents
