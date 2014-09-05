#!python
"""
fsic
====
Tools for Stock-Flow Consistent macroeconomic modelling.

"""


import argparse

from FSIC import __version__ as version


# Create top-level parser
parser = argparse.ArgumentParser(
    description='Tools for Stock-Flow Consistent macroeconomic modelling.',
    fromfile_prefix_chars='@')
parser.add_argument(
    '-V', '--version',
    action='version',
    version=version)

# Add sub-parsers
subparsers = parser.add_subparsers(
    title='commands',
    dest='command')

# 'Build' sub-parser
parser_build = subparsers.add_parser(
    'build',
    help='build a model from one or more source files')
parser_build.add_argument(
    '-o', '--output',
    nargs=1,
    metavar='OUTPUT',
    default=None,
    type=str,
    required=False,
    help='set model name (exclude file extension)')
parser_build.add_argument(
    'files',
    nargs='+',
    metavar='FILE',
    type=str,
    help='list of files that define the model')


# Main
if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'build':
        from fsic.tools.build import Build
        b = Build()
        b.read_files(list(args.files))
        script = b.build()
        if args.output is None:
            print(script)
        else:
            with open(args.output[0], 'wt') as f:
                f.write(script)
