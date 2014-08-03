#!python
"""
fsic-build
==========
FSIC script to generate models from user-defined specification files.

"""


import argparse

from fsic import __version__ as version

from fsic.tools.build import Build
from fsic.parser.chunk import parse
from fsic.parser.code import translate, identify_variables


parser = argparse.ArgumentParser(
    description='FSIC model builder.',
    fromfile_prefix_chars='@')
parser.add_argument(
    '-V', '--version',
    action='version',
    version=version)

parser.add_argument(
    '-o', '--output',
    nargs=1,
    metavar='OUTPUT',
    default=None,
    type=str,
    required=False,
    help='set model name (exclude file extension)')

parser.add_argument(
    'files',
    nargs='+',
    metavar='FILE',
    type=str,
    help='list of files that define the model')


if __name__ == '__main__':
    # Parse arguments
    args = parser.parse_args()
    # Initialise new Build object
    b = Build()
    # Read in file by file and flatten code-block list
    for f in args.files:
        b.read_file(f)
    # Parse to a list of Dictionary objects
    blocks = [parse(c) for c in b.chunks]
    # Extract Python code only and translate
    python_code = [b['code'] for b in blocks if 'python' in b['classes']]
    python_code = '\n'.join(python_code)
    python_code = translate(python_code)
    # Identify variable names and generate initialisation code
    variables = identify_variables(python_code)
    variables = variables['endogenous'] + variables['exogenous']
    initialisation = [v + ' = Series(default_value, index=span, dtype=np.float64)'
                      for v in variables]
    initialisation = '\n'.join(initialisation)
