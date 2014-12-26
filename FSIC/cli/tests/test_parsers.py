# -*- coding: utf-8 -*-


import FSIC.cli.parsers


def test_solve_parser():
    parser = FSIC.cli.parsers.create_parser('Test parser')
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command')
    subparsers = FSIC.cli.parsers.add_subparser_solve(subparsers)
    args = parser.parse_args(['solve',
                              '--span', '1957', '2010'])
    assert args.__dict__ == {
        'solve_from': None,
        'verbose': False,
        'set': None,
        'input': None,
        'output': None,
        'define': None,
        'span': [1957, 2010],
        'command': 'solve'}


if __name__ == '__main__':
    import nose
    nose.runmodule()
