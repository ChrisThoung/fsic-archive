# -*- coding: utf-8 -*-
"""
script
======
Interface for main 'fsic.py' script.

"""

import argparse

from fsic.build.model import ORDER_METHODS
from fsic.metadata import VERSION

from fsic.exceptions import FSICError


PARSER = argparse.ArgumentParser(
    description='Tools for Stock-Flow Consistent macroeconomic modelling.',
    fromfile_prefix_chars='@')

PARSER.add_argument('-V', '--version',
                    action='version',
                    version=VERSION)


SUBPARSERS = PARSER.add_subparsers(title='commands',
                                   dest='cmd')


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

METHODS = list(ORDER_METHODS.keys())
PARSER_BUILD.add_argument('--order-method',
                          metavar='METHOD',
                          type=str,
                          choices=METHODS,
                          default=METHODS[0],
                          help='method to use to order '
                          'the equations of the system {}'.format(
                              '{' + ','.join(METHODS) + '}'))


def handle_args(args):
    """Main argument handler for 'fsic' script."""
    try:
        args = args.__dict__
    except AttributeError:
        pass

    cmd = args['cmd']
    if cmd == 'build':
        _build(args)
    else:
        raise ValueError('Unrecognised command: {}'.format(cmd))


def _build(args):
    from fsic.parser.markdown import read_markdown
    from fsic.classes.schematic import Schematic
    from fsic.build.model import build_model

    schematics = list(filter(
        lambda x: False if x is None else True,
        [read_markdown(f) for f in args['files']]))

    combined = Schematic.merge(schematics)
    if combined.block_table.index.tolist() == ['_Frontmatter']:
        raise FSICError('No code found in source file(s)')

    script = build_model(combined,
                         'script',
                         with_main=True,
                         order_method=args['order_method'])

    output = args['output']
    if output is None:
        print(script)
    else:
        with open(output[0], 'w') as f:
            print(script, file=f)


def interface():
    handle_args(PARSER.parse_args())
