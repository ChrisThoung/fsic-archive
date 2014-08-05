#!python
"""
fsic-build
==========
FSIC script to generate models from user-defined specification files.

"""


import argparse

from fsic import __version__ as version

from fsic.tools.build import Build


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
    b.read_files(list(args.files))
    # Generate output
    script = b.build()
    if args.output is None:
        print(script)
    else:
        with open(args.output, 'wt') as f:
            f.write(script)
