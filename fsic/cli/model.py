# -*- coding: utf-8 -*-
"""
model
=====
Interface for individual model scripts.

"""

import argparse
import itertools
import os
import re

from fsic.io.api import read
from fsic.io.csvy import write_csvy


def make_cli(cls):
    """Create `parser` (`ArgumentParser`) and `handle_args()` function.

    Parameter
    ---------
    cls : model class definition
        Typically derived from FSIC `Model` class

    """
    return _make_parser(cls), _make_handler(cls)


def _make_parser(cls):
    parser = argparse.ArgumentParser(
        description=cls.__doc__,
        fromfile_prefix_chars='@')

    parser.add_argument('-V', '--version',
                        action='version',
                        version=cls.VERSION)


    subparsers = parser.add_subparsers(title='commands',
                                       dest='cmd')


    parser_solve = subparsers.add_parser('solve')

    # Arguments to control span of model database
    arguments = [['--start', 'first period of model database'],
                 ['--end', 'last period of model database'],
                 ['--solve-from', 'first period to solve'],
                 ['--solve-to', 'last period to solve'], ]
    for a in arguments:
        parser_solve.add_argument(a[0],
                                  nargs='?',
                                  metavar='PERIOD',
                                  type=str,
                                  default=None,
                                  help=a[1])

    parser_solve.add_argument('-f', '--input',
                              nargs='+',
                              metavar='INPUT',
                              type=str,
                              default=None,
                              help='input file(s) of model data')
    parser_solve.add_argument('-o', '--output',
                              nargs='+',
                              metavar='OUTPUT',
                              type=str,
                              default=None,
                              help='output file(s) for model results')

    parser_solve.add_argument('-c', '--command',
                              nargs='+',
                              metavar='EXPR',
                              type=str,
                              default=None,
                              help='variable assignments to make before solution (uses `exec()`)',
                              action='append')

    parser_solve.add_argument('-v', '--verbose',
                              default=0,
                              help='print solution progress '
                                   '(use repeatedly to increase level of detail)',
                              action='count')
    return parser


def _make_handler(cls):
    def handle_args(args, *, return_result=True):
        """Argument handler for model scripts."""
        try:
            args = args.__dict__
        except AttributeError:
            pass

        cmd = args['cmd']
        if cmd == 'solve':
            result = _solve(args, cls, return_result=return_result)
        else:
            raise ValueError('Unrecognised command: {}'.format(cmd))

        if return_result:
            return result

    return handle_args


def translate(expression, prefix='model.'):
    """Convert `expression` to a compatible Python statement."""
    # Regular expression to identify terms in the expression
    pattern = re.compile(r'''
        (?:
            (?P<variable>(?P<name>[_A-Za-z][_A-Za-z0-9]*)\s*(?:[[](?P<index>.*?)[]])?) |
            (?P<value>(?:[0-9]+(?:[.]?[0-9]*)?)|(?:[.][0-9]+))
        )
    ''', re.VERBOSE)

    # Generate a template to re-insert the terms
    template = re.sub(r'\s+', ' ', pattern.sub(' {} ', expression).strip())

    # Identify terms and modify, if necessary
    terms = []
    for m in pattern.finditer(expression):
        gd = m.groupdict()

        if gd['variable'] is not None:
            term = '{}{}'.format(prefix, gd['name'])
            if gd['index']:
                term += '[{}]'.format(gd['index'])
        elif gd['value'] is not None:
            term = gd['value']
        else:
            raise ValueError

        terms.append(term)

    expression = template.format(*terms)
    return expression


def _solve(args, cls, *, return_result=True):
    """Solve an instance of `cls` using the settings in `args`.

    ** Warning: if `args` is non-empty, this function uses `exec()` to assign
                values to model variables. **

    """
    data = None
    input_ = args['input']
    if input_:
        data = read(input_, index_col=0)

    model = cls(start=args['start'], end=args['end'],
                solve_from=args['solve_from'], solve_to=args['solve_to'],
                data=data)

    if args['command']:
        commands = '\n'.join([translate(c.strip())
                              for c in itertools.chain.from_iterable(
                                      args['command'])])
        exec(commands)

    model.solve(verbosity=args['verbose'])

    output = args['output']
    if output:
        for path in output:
            if os.path.splitext(path)[1] in ('.csv', '.csvy'):
                write_csvy(model.data, path)
            else:
                raise ValueError(
                    'Unrecognised file extension in: {}'.format(path))
    elif return_result:
        return model
    else:
        print(model.data.to_string())
