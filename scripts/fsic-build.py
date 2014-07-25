#!python
"""
fsic-build
==========
FSIC script to generate models from user-defined specification files.

"""


import argparse
from fsic import __version__ as version


parser = argparse.ArgumentParser(
    description='FSIC model builder.',
    fromfile_prefix_chars='@')
parser.add_argument(
    '-V', '--version',
    action='version',
    version=version)

parser.add_argument(
    'files',
    metavar='FILE',
    type=str,
    nargs='+',
    help='list of files that define the model')


if __name__ == '__main__':
    args = parser.parse_args()
