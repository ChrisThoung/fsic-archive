# -*- coding: utf-8 -*-
"""
Build
=====
FSIC tool class to generate the Python script and accompanying files for a
macroeconomic model.

"""


import configparser
import os

from FSIC import __version__ as version


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
        from FSIC.parser.markdown import extract
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
        insert_code()
        insert_info()

        """
        # Extract template script
        with open(self.model_template, 'rt') as f:
            script = f.read()
        # Insert code and other information into template
        script = self.insert_code(script)
        # Insert other information
        script = self.insert_info(script)
        # Return
        return script

    def insert_code(self, script):
        """Insert Python code blocks into script.

        Parameters
        ==========
        script : string
            Script containing markers for replacement

        Returns
        =======
        script : string
            Copy of `script` with markers replaced with code

        See also
        ========
        parse_chunks()
        build_initialise()
        build_endogenous_variables()
        build_results()

        FSIC.utilities.string.indent_lines()

        """
        # Generate class code
        equations = self.parse_chunks()
        initialise = self.build_initialise(equations)
        endogenous = self.build_endogenous_variables(equations)
        results = self.build_results(equations)
        # Insert into `script`
        from FSIC.utilities.string import indent_lines
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

    def insert_info(self, script):
        """Insert Python code blocks into script.

        Parameters
        ==========
        script : string
            Script containing markers for replacement

        Returns
        =======
        script : string
            Copy of `script` with markers replaced with code

        See also
        ========
        parse_chunks()
        get_descriptors()

        FSIC.utilities.string.indent_lines()
        FSIC.utilities.string.wrap_lines()

        """
        # Extract model information
        cfg = self.parse_chunks(classes='ini', language='ini')
        cfg = self.get_descriptors(cfg)
        # Insert into `script`
        from FSIC.utilities.string import indent_lines, wrap_lines
        # Model name and accompanying version information
        script = script.replace('___MODEL___', cfg['name'])
        script = script.replace(
            '___NAME___',
            cfg['name'] + '\n' + ('=' * len(cfg['name'])))
        script = script.replace(
            '___FSIC_VERSION___',
            'Model version: ' + cfg['version'] + '\n' +
            'Generated by FSIC version: ' + version)
        model_version = '''\
self.MAJOR = %d
self.MINOR = %d
self.PATCH = %d
self.VERSION = \'%s\'
self.FSIC_BUILD = \'%s\'
''' % (
    int(cfg['major']),
    int(cfg['minor']),
    int(cfg['patch']),
    cfg['version'],
    version)
        model_version = indent_lines(
            model_version,
            num_tabs=2,
            skip_first_line=True)
        script = script.replace(
            '___MODEL_VERSION___',
            model_version)
        # Module docstring
        module_docstring = 'Implementation of class %s: %s.' % (
            cfg['name'], cfg['description'])
        module_docstring = wrap_lines(module_docstring, line_length=80)
        script = script.replace(
            '___MODULE_DOCSTRING___',
            module_docstring)
        # Short description: one-sentence description of the model class
        short_description = 'Class definition for %s: %s' % (
            cfg['name'], cfg['description'])
        if not short_description.endswith('.'):
            short_description += '.'
        script = script.replace(
            '___SHORT_DESCRIPTION___',
            short_description)
        # Long description: reference to further documentation/information
        long_description = wrap_lines(
            cfg['reference'],
            line_length=72)
        long_description = indent_lines(long_description)
        long_description = 'For more information, see:\n' + long_description
        long_description = indent_lines(
            long_description,
            skip_first_line=True)
        script = script.replace(
            '___LONG_DESCRIPTION___',
            long_description)
        # Return
        return script

    def parse_chunks(self, classes=['python'], language='python'):
        """Parse `self.chunks` with attributes matching `classes`.

        Parameters
        ==========
        classes : string or list of strings
            Classes to match against those in `self.chunks`
        language : string
            Programming language of code blocks to be parsed

        See also
        ========
        FSIC.parser.chunk.parse()
        FSIC.parser.code.translate()
        FSIC.parser.ini.read_string()

        """
        # Remove duplicates
        chunks = list(sorted(list(set(self.chunks))))
        # Parse chunks to extract metadata
        from FSIC.parser.chunk import parse
        blocks = [parse(c) for c in chunks]
        # Filter by classes
        if type(classes) is not list:
            classes = [classes]
        blocks = [b for b in blocks
                  if len(set(b['classes']) & set(classes))]
        # Extract code
        code_blocks = [b['code'] for b in blocks]
        code = '\n'.join(code_blocks)
        # Parse
        if language == 'python':
            from FSIC.parser.code import translate
            code = translate(code)
        elif language == 'ini':
            from FSIC.parser.ini import read_string
            code = read_string(code)
        else:
            raise ValueError(
                'Unrecognised language argument \'%s\'' % (language))
        # Return
        return code

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
        FSIC.parser.code.identify_variables()

        """
        from FSIC.parser.code import identify_variables
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
        FSIC.parser.code.identify_variables()

        """
        from FSIC.parser.code import identify_variables
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
        FSIC.parser.code.identify_variables()

        """
        from FSIC.parser.code import identify_variables
        variables = identify_variables(code)
        variables = variables['endogenous'] + variables['exogenous']
        results = 'results = DataFrame({' + '\n\t' + (
            ',\n\t'.join(
                ['\'' + v.replace('self.', '') + '\': ' + v
                 for v in variables]) + '})')
        return results

    def get_descriptors(self, cfg, section='DEFAULT'):
        """Return the relevant section of `cfg` with derived information added.

        Parameters
        ==========
        cfg : ConfigParser object
            ConfigParser object of settings/descriptors
        section : string
            Section name from `cfg` to extract

        Returns
        =======
        extract : ConfigParser section object
            Subset of `cfg`, with additional derived information

        """
        # Extract `section`
        extract = cfg[section]
        # Form model version number (adding 'dev' as required)
        extract['version'] = '%d.%d.%d' % (
            int(extract['major']),
            int(extract['minor']),
            int(extract['patch']))
        if extract.getboolean('dev'):
            extract['version'] = extract['version'] + '.dev'
        # Return
        return extract
