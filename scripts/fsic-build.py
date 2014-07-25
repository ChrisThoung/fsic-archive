#!python
"""
fsic-build
==========
FSIC script to generate models from user-defined specification files.

"""


import argparse

from fsic import __version__ as version

from fsic.parser.markdown import extract
from fsic.parser.chunk import parse
from fsic.parser.code import translate


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
    # Read in file by file and flatten code-block list
    chunks = [extract(open(f, 'rt').read()) for f in args.files]
    chunks = [i for c in chunks for i in c]
    # Parse to a list of Dictionary objects
    blocks = [parse(c) for c in chunks]
    # Extract Python code only and translate
    python_code = [b['code'] for b in blocks if 'python' in b['classes']]
    python_code = '\n'.join(python_code)
    python_code = translate(python_code)
