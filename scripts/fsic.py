#!/usr/bin/python3
"""
fsic
====
Tools for Stock-Flow Consistent macroeconomic modelling.

"""


import argparse
import os

from FSIC import __version__ as version
from FSIC.utilities.os import templates


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

# 'Template' sub-parser
parser_template = subparsers.add_parser(
    'template',
    help='print a template script for manual editing')
parser_template.add_argument(
    '-o', '--output',
    nargs=1,
    metavar='OUTPUT',
    default=None,
    type=str,
    required=False,
    help='file to direct output to')
parser_template.add_argument(
    'template',
    choices=list(templates.keys()),
    nargs=1,
    metavar='TEMPLATE',
    type=str,
    help='template to access')


# Main
if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'build':
        from FSIC.tools.build import Build
        b = Build()
        b.read_files(list(args.files))
        script = b.build()
        if args.output is None:
            print(script)
        else:
            with open(args.output[0], 'wt') as f:
                f.write(script)
    elif args.command == 'template':
        from FSIC.utilities.os import package_path
        path = templates[args.template[0]]
        with open(os.path.join(package_path, path), 'rt') as f:
            template = f.read()
        if args.output is None:
            print(template)
        else:
            with open(args.output[0], 'wt') as f:
                f.write(template)
