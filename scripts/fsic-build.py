#!python


import argparse
from fsic import __version__ as version


parser = argparse.ArgumentParser(
    description='FSIC model builder.',
    fromfile_prefix_chars='@')
parser.add_argument('-V', '--version', action='version', version=version)


if __name__ == '__main__':
    args = parser.parse_args()
