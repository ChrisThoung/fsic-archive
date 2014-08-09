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
        # Set templates path and form model and linker filepaths
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates')
        self.model_template = os.path.join(template_path, 'model.py')
        self.linker_template = os.path.join(template_path, 'linker.py')
        # Initialise variables
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
        """Build the final model script and return as a string.

        See also
        ========
        parse_chunks()
        build_initialise()
        build_endogenous_variables()
        build_results()

        fsic.utilities.string.indent_lines()

        """
        # Generate class code
        equations = self.parse_chunks()
        initialise = self.build_initialise(equations)
        endogenous = self.build_endogenous_variables(equations)
        results = self.build_results(equations)
        # Extract template script
        with open(self.model_template, 'rt') as f:
            script = f.read()
        # Insert code
        from fsic.utilities.string import indent_lines
        script = script.replace(
            '___INITIALISE___',
            indent_lines(initialise, num_tabs=2, skip_first_line=True))
        script = script.replace(
            '___SOLVE_EQUATIONS___',
            indent_lines(equations, num_tabs=2, skip_first_line=True))
        script = script.replace(
            '___GET_ENDOGENOUS_VARIABLE_VALUES___',
            indent_lines(endogenous, num_tabs=2, skip_first_line=True))
        script = script.replace(
            '___GET_RESULTS___',
            indent_lines(results, num_tabs=2, skip_first_line=True))
        # Return
        return script

    def build_initialise(self, code):
        """Return code to initialise the variables of a model.

        Parameters
        ==========
        code : string
            Code script containing all model variables

        Returns
        =======
        initialise : string
            Python code to initialise model variables

        See also
        ========
        fsic.parser.code.identify_variables()

        """
        from fsic.parser.code import identify_variables
        variables = identify_variables(code)
        variables = variables['endogenous'] + variables['exogenous']
        initialise = [v + (' = Series(default, '
                           'index=self.full_span, '
                           'dtype=np.float64)')
                      for v in variables]
        initialise = '\n'.join(initialise)
        return initialise

    def build_endogenous_variables(self, code):
        """Return code to store endogenous variable values.

        Parameters
        ==========
        code : string
            Code script containing endogenous model variables

        Returns
        =======
        variables : string
            Python code to insert endogenous variable values into a Dictionary

        See also
        ========
        fsic.parser.code.identify_variables()

        """
        from fsic.parser.code import identify_variables
        variables = identify_variables(code)
        variables = variables['endogenous']
        variables = [('values[\'' +
                      v.replace('self.', '') +
                      '\'] = ' + v + '[period]')
                     for v in variables]
        variables = '\n'.join(variables)
        return variables

    def build_results(self, code):
        """Return code to return model results as a DataFrame.

        Parameters
        ==========
        code : string
            Code script containing all model variables

        Returns
        =======
        results : string
            Python code to generate a results DataFrame

        See also
        ========
        fsic.parser.code.identify_variables()

        """
        from fsic.parser.code import identify_variables
        variables = identify_variables(code)
        variables = variables['endogenous'] + variables['exogenous']
        results = 'results = DataFrame({' + '\n\t' + (
            ',\n\t'.join(
                ['\'' + v.replace('self.', '') + '\': ' + v
                 for v in variables]) + '})')
        return results

    def parse_chunks(self, classes=['python'], language='python'):
        """Parse `self.chunks` with attributes matching `classes`.

        Parameters
        ==========
        classes : list of strings
            Classes to match against those in `self.chunks`
        language : string
            Programming language of code blocks to be parsed

        See also
        ========
        fsic.parser.chunk.parse()
        fsic.parser.code.translate()
        fsic.parser.ini.read_string()

        """
        # Remove duplicates
        chunks = list(set(self.chunks))
        # Parse chunks to extract metadata
        from fsic.parser.chunk import parse
        blocks = [parse(c) for c in chunks]
        # Filter by classes
        blocks = [b for b in blocks if len(set(b['classes']) & set(classes))]
        # Extract code
        code_blocks = [b['code'] for b in blocks]
        code = '\n'.join(code_blocks)
        # Parse
        if language == 'python':
            from fsic.parser.code import translate
            code = translate(code)
        elif language == 'ini':
            from fsic.parser.ini import read_string
            code = read_string(code)
        else:
            raise ValueError(
                'Unrecognised language argument \'%s\'' % (language))
        # Return
        return code
