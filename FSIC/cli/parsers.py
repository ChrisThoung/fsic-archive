# -*- coding: utf-8 -*-
"""
parsers
=======
FSIC `argparse` ArgumentParsers for command-line operations.

"""


def add_subparser_solve(subparsers):
    """Add a 'solve' option to `subparsers`.

    Parameters
    ==========
    subparsers : argparse ArgumentParser special action object
        Special action object generated from a call to:
            `argparse.ArgumentParser.add_subparsers()

    Returns
    =======
    subparsers : argparse ArgumentParser special action object
        Updated version of `subparsers`

    """
    # Initialise subparser
    parser_solve = subparsers.add_parser(
        'solve',
        help='solve the model')
    # Add 'verbose' argument
    parser_solve.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='print detailed solution output (not yet implemented)')
    # Add 'input' and 'output' file arguments
    parser_solve.add_argument(
        '-f', '--input',
        nargs='+',
        metavar='INPUT',
        default=None,
        type=str,
        required=False,
        help='input file(s) for model data')
    parser_solve.add_argument(
        '-o', '--output',
        nargs='+',
        metavar='OUTPUT',
        default=None,
        type=str,
        required=False,
        help='output file(s) for model results')
    # Add 'define' and 'set' arguments
    parser_solve.add_argument(
        '-D', '--define',
        action='append',
        nargs='+',
        metavar='PARAMETER',
        default=None,
        type=str,
        required=False,
        help='set (time-invariant) model parameters')
    parser_solve.add_argument(
        '--set',
        action='append',
        nargs='+',
        metavar='EXPRESSION',
        default=None,
        type=str,
        required=False,
        help='set (time-varying) model variables prior to run')
    # Add 'span' and 'past' arguments
    parser_solve.add_argument(
        '--span',
        nargs=2,
        metavar='PERIOD',
        default=None,
        type=int,
        required=True,
        help='set the start and end periods that define the span of the model')
    parser_solve.add_argument(
        '--solve-from',
        metavar='PERIOD',
        default=None,
        type=int,
        required=False,
        help=('set the first period (within the model\'s span) to solve; '
              'default is the first period of the span'))
    # Return
    return subparsers
