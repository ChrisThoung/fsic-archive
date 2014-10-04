# -*- coding: utf-8 -*-


import datetime

from nose.tools import raises

from FSIC.utilities.date import DateParser


def test_parse():
    test_cases = {
        '2000': [2000, 1, 1, 'A'],
        '2000A1': [2000, 1, 1, 'A'],
        '2000A01': [2000, 1, 1, 'A'],

        '2005Q2': [2005, 2, 4, 'Q'],
        '2005Q02': [2005, 2, 4, 'Q'],

        '2010M9': [2010, 9, 12, 'M'],
        '2010M09': [2010, 9, 12, 'M'],
    }
    for case, expected in test_cases.items():
        parser = DateParser(case)
        result = [parser.year,
                  parser.period,
                  parser.freq,
                  parser.freq_id]
        assert result == expected


@raises(ValueError)
def test_parse_unrecognised_frequency():
    DateParser('1995Z1')


def test_to_datetime():
    test_cases = {
        '2000': datetime.datetime(2000, 1, 1),
        '2000A1': datetime.datetime(2000, 1, 1),

        '2005Q2': datetime.datetime(2005, 4, 1),
        '2005Q02': datetime.datetime(2005, 4, 1),

        '2010M9': datetime.datetime(2010, 9, 1),
        '2010M09': datetime.datetime(2010, 9, 1),
    }
    for case, expected in test_cases.items():
        parser = DateParser(case)
        assert parser.to_datetime() == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
