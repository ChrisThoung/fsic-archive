# -*- coding: utf-8 -*-
"""
ini
===
FSIC parser to handle INI-style configuration file strings.

"""


def with_prefix(input, prefix='[DEFAULT]\n'):
    """Prefix `input` with `prefix`, if not already present.

    Parameters
    ==========
    input : string
        Configuration data to modify
    prefix : string
        Prefix to test for and add, if necessary

    Returns
    =======
    output : string
        Copy of `input`, with `prefix` added if necessary.

    """
    if input.strip().startswith(prefix):
        output = input
    else:
        output = prefix + input
    return output
