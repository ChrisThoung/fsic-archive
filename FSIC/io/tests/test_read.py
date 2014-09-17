# -*- coding: utf-8 -*-


import FSIC.io.read


def test_detect_filetype_exts():
    test_data = {
        'input.csv': 'csv',
        'input.csv.gz': 'csv.gz',
        'input.data.csv.gz': 'csv.gz',
        'input.csv.data.csv': 'csv',
        'input.csv.csv': 'csv',
        'input.csv.tsv': 'tsv',
        'input.gz.csv': 'csv',
        'input.csv.tsv.csv': 'csv',
    }
    for input, expected in test_data.items():
        assert FSIC.io.read.read(input) == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
