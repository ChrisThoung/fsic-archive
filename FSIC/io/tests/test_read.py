# -*- coding: utf-8 -*-


import os
import zipfile

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

from nose.tools import raises

import FSIC.io.read
from FSIC.settings import dtype


test_dir = os.path.dirname(__file__)


def test_clean_file_ext():
    test_data = {
        '.csv': 'csv',
        'csv': 'csv',
        '.': '',
        'a': 'a',
        '.a': 'a',
    }
    for input, expected in test_data.items():
        output = FSIC.io.read.clean_file_ext(input)
        assert output == expected


def test_filetype():
    test_data = {
        # Uncompressed files: Should only identify the extension
        'input.csv': {'format': 'csv'},
        'input.tsv': {'format': 'tsv'},
        'input.csv.tsv': {'format': 'tsv'},
        # Compressed file: Should identify the compression type and the 'main'
        # file extension
        'input.csv.gz':
            {'format': 'csv', 'compression': 'gz'},
        # Filenames containing many dots should make no difference
        'many.descriptors.separated.by.dots.csv':
            {'format': 'csv'},
        'many.descriptors.separated.by.dots.csv.gz':
            {'format': 'csv', 'compression': 'gz'},
        'many.descriptors.separated.by.dots.zip':
            {'compression': 'zip'},
        # Archive files: Identify the compression type only
        'archive.zip': {'compression': 'zip'},
        # Compression formats in the middle of the path are ignored
        'extracted.from.gz.csv' : {'format': 'csv'},
        'extracted.from.zip.csv' : {'format': 'csv'},
        # No file extension: `None`
        'missing_file_ext': None,
        # Dot files: `None`
        '.csv': None,
        '.tsv': None,
        '.gz': None,
        '.zip': None,
        # Dot file with extension: As normal
        '.csv.tsv': {'format': 'tsv'},
        '.csv.tsv.gz': {'format': 'tsv', 'compression': 'gz'},
        # Dot file with a compressed-file extension: `None` (consistent with
        # uncompressed dot files treatment)
        '.csv.gz': None,
    }
    for input, expected in test_data.items():
        output = FSIC.io.read.filetype(input)
        assert output == expected
        with_folder = FSIC.io.read.filetype(
            os.path.join('model', 'data', input))
        assert with_folder == expected


def test_read_csv():
    input = os.path.join(test_dir, 'data', 'table.csv')
    result = FSIC.io.read.read(input)
    expected = pd.read_csv(input, index_col='index', dtype=dtype)
    assert_frame_equal(result[0], expected)


def test_read_zip():
    # Create a new zip file
    path = os.path.join(test_dir, 'data', 'test.zip')
    try:
        os.remove(path)
    except:
        pass
    with zipfile.ZipFile(path, 'w') as z:
        z.write(
            os.path.join(test_dir, 'data', 'table.csv'),
            arcname='table.csv')
        z.write(
            os.path.join(test_dir, 'data', 'table.tsv'),
            arcname='table.tsv')
    # Read
    result = FSIC.io.read.read(path)
    expected = [pd.read_csv(
                    os.path.join(test_dir, 'data', 'table.csv'),
                    index_col='index', dtype=dtype),
                pd.read_csv(
                    os.path.join(test_dir, 'data', 'table.csv'),
                    index_col='index', dtype=dtype)]
    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert_frame_equal(r, e)


def test_read_csv_specify_method():
    input = os.path.join(test_dir, 'data', 'actually_tsv.csv')
    result = FSIC.io.read.read(input, method='tsv')
    expected = pd.read_csv(input, sep='\t', index_col='index', dtype=dtype)
    assert_frame_equal(result[0], expected)


def test_read_csv_specify_method_to_clean():
    input = os.path.join(test_dir, 'data', 'actually_tsv.csv')
    result = FSIC.io.read.read(input, method='.tsv')
    expected = pd.read_csv(input, sep='\t', index_col='index', dtype=dtype)
    assert_frame_equal(result[0], expected)


@raises(ValueError)
def test_read_csv_no_method_error():
    FSIC.io.read.read('no_file_ext')


def test_read_csv_no_method_no_error():
    assert FSIC.io.read.read('no_file_ext', fail_on_error=False) is None


if __name__ == '__main__':
    import nose
    nose.runmodule()
