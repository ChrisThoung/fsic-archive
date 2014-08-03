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
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates')
        self.model_template = os.path.join(template_path, 'model.py')
        self.linker_template = os.path.join(template_path, 'linker.py')
        self.chunks = []

    def read_file(self, path):
        """Read in the chunks from the file in `path`.

        Parameters
        ==========
        path : string
            Location of file to parse, containing Markdown-formatted code

        Notes
        =====
        This function reads the contents of `path` and passes them to
        read_string() for processing.

        """
        with open(path, 'rt') as f:
            self.read_string(f.read())

    def read_string(self, script):
        """Extract and store the chunks contained in the string `script`.

        Parameters
        ==========
        script : string
            Markdown-formatted string to parse

        Notes
        =====
        This function extracts the chunks defined in `script` and *appends*
        them to the variable `chunks`

        """
        from fsic.parser.markdown import extract
        self.chunks = self.chunks + extract(script)
