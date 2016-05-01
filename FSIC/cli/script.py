# -*- coding: utf-8 -*-
"""
script
======
Interface for main 'fsic.py' script.

"""

import argparse

from FSIC.build.model import ORDER_METHODS
from FSIC.metadata import VERSION


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
    """Main argument handler for FSIC script."""
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
    from FSIC.parser.markdown import read_markdown
    from FSIC.build.model import build_model

    input_files = args['files']
    if len(input_files) != 1:
        raise NotImplementedError(
            'Currently, can only process one file at a time')

    script = build_model(read_markdown(input_files[0]),
                         'script',
                         with_main=True,
                         order_method=args['order_method'])

    output = args['output']
    if output is None:
        print(script)
    else:
        with open(output[0], 'w') as f:
            print(script, file=f)
