# -*- coding: utf-8 -*-
"""
script
======
Interface for main 'fsic.py' script.

"""

import argparse

from FSIC.metadata import VERSION


PARSER = argparse.ArgumentParser(
    description='Tools for Stock-Flow Consistent macroeconomic modelling.',
    fromfile_prefix_chars='@')

PARSER.add_argument('-V', '--version',
                    action='version',
                    version=VERSION)


SUBPARSERS = PARSER.add_subparsers(title='commands',
                                   dest='command')


PARSER_BUILD = SUBPARSERS.add_parser('build')

PARSER_BUILD.add_argument('files',
                          nargs='+',
                          metavar='FILE',
                          type=str,
                          help='model-definition input file(s)')

PARSER_BUILD.add_argument('-o', '--output',
                          nargs=1,
                          metavar='OUTPUT',
                          type=str,
                          help='output file (otherwise print to stdout)')


def handle_args(args):
    """Main argument handler for FSIC script."""
    try:
        args = args.__dict__
    except:
        pass

    command = args['command']
    if command == 'build':
        _build(args)
    else:
        raise ValueError('Unrecognised command: {}'.format(command))


def _build(args):
    from FSIC.parser.markdown import read_markdown
    from FSIC.build.model import build_model

    input_files = args['files']
    if len(input_files) != 1:
        raise NotImplementedError(
            'Currently, can only process one file at a time')

    script = build_model(read_markdown(input_files[0]), 'script')

    output = args['output']
    if output is None:
        print(script)
    else:
        with open(output[0], 'w') as f:
            print(script, file=f)
