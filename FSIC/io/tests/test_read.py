# -*- coding: utf-8 -*-


import FSIC.io.read


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
        'input.csv': {'format': 'csv', 'compression': ''},
        'input.csv.gz': {'format': 'csv', 'compression': 'gz'},
        'input.data.csv.gz': {'format': 'csv', 'compression': 'gz'},
        'input.csv.data.csv': {'format': 'csv', 'compression': ''},
        'input.csv.csv': {'format': 'csv', 'compression': ''},
        'input.csv.tsv': {'format': 'tsv', 'compression': ''},
        'input.gz.csv': {'format': 'csv', 'compression': ''},
        'input.csv.tsv.csv': {'format': 'csv', 'compression': ''},
    }
    for input, expected in test_data.items():
        output = FSIC.io.read.detect_filetype(input)
        assert output == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
