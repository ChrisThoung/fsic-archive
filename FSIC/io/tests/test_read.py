# -*- coding: utf-8 -*-


import os

import pandas as pd
from pandas.util.testing import assert_frame_equal

import FSIC.io.read


test_dir = os.path.dirname(__file__)


def test_clean_file_ext():
    test_data = {
        '.csv': 'csv',
        'csv': 'csv',
    }
    for input, expected in test_data.items():
        output = FSIC.io.read.clean_file_ext(input)
        assert output == expected


def test_detect_filetype_exts():
    test_data = {
        # Standard formats, whether compressed or not
        'input.csv': {'format': 'csv'},
        'input.csv.gz': {'format': 'csv', 'compression': 'gz'},
        'input.data.csv.gz': {'format': 'csv', 'compression': 'gz'},
        'input.csv.data.csv': {'format': 'csv'},
        'input.csv.csv': {'format': 'csv'},
        'input.csv.tsv': {'format': 'tsv'},
        'input.gz.csv': {'format': 'csv'},
        'input.csv.tsv.csv': {'format': 'csv'},
        # Zip archives
        'no_further_ext_required.zip': {'compression': 'zip'},
        # Invalid filepaths evaluate to `None`
        'no_file_ext': None,
        'invalid_file_ext.not_a_type': {'format': 'not_a_type'},
        # Dot files, with no filename, should evaluate to `None`
        '.csv': None,
        '.tsv': None,
        '.zip': None,
    }
    for input, expected in test_data.items():
        output = FSIC.io.read.detect_filetype(input)
        assert output == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
