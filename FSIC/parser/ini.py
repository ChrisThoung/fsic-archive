# -*- coding: utf-8 -*-
"""
ini
===
FSIC parser to handle INI-style configuration file strings.

"""


import configparser


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


def read_string(ini):
    """Return a ConfigParser object from the contents of `ini`.

    Parameters
    ==========
    ini : string
        Configuration data to parse

    Returns
    =======
    cfg : ConfigParser object
        Parsed configuration data

    """
    ini = with_prefix(ini)
    cfg = configparser.ConfigParser()
    cfg.read_string(ini)
    return cfg
