# -*- coding: utf-8 -*-
"""
Build
=====
FSIC tool class to generate the Python script and accompanying files for a
macroeconomic model.

"""


import configparser
import os


class Build:
    """FSIC class to generate macroeconomic models from user-supplied inputs.

    """

    def __init__(self):
        self.model_template = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates',
            'model.py')

    def read_file(self, path):
        pass

    def read_string(self, script):
        pass
