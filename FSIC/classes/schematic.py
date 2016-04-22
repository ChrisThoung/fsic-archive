# -*- coding: utf-8 -*-
"""
schematic
=========
`Schematic` class to store complete model specifications.

"""

class Schematic(object):
    """FSIC class to store a complete model specification."""

    def __init__(self):
        self.block_table = None
        self.equations = None
        self.equation_table = None
        self.symbol_table = None
