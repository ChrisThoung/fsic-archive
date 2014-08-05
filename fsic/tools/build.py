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

    def read_files(self, files):
        """Read in the chunks from the filepaths in `files`.

        Parameters
        ==========
        files : list of strings
            List of files to parse

        See also
        ========
        read_file()

        """
        for f in files:
            self.read_file(f)

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

        See also
        ========
        read_string()

        """
        with open(path, 'rt') as f:
            self.read_string(f.read())

    def read_string(self, script):
        """Extract and store the chunks contained in the string `script`.

        Parameters
        ==========
        script : string
            Markdown-formatted string to parse

        See also
        ========
        add_chunks()

        """
        from fsic.parser.markdown import extract
        self.add_chunks(extract(script))

    def add_chunks(self, chunks):
        """Store `chunks`.

        Parameters
        ==========
        chunks : list of strings
            Chunks to store for parsing

        Notes
        =====
        This function *appends* `chunks` to `self.chunks`. It does not test
        for duplicates.

        """
        self.chunks = self.chunks + chunks

    def build(self):
        """Build the final model script and return as a string."""
        with open(self.model_template, 'rt') as f:
            script_template = f.read()
