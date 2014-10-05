# -*- coding: utf-8 -*-
"""
date
====
FSIC utility functions to handle time indexes.

"""


import datetime
import re

from pandas import DatetimeIndex


class DateParser:
    """FSIC class to process period strings such as '2014Q1'."""

    def __init__(self, date):
        """Constructor: parse `date`.

        Parameters
        ==========
        date : string
            Date string to parse

        Returns
        =======
        N/A

        """
        # Define the mapping from period string to number of periods
        self.freq_map = {
            'A': 1,
            'Q': 4,
            'M': 12,
        }
        # Parse `date`
        self.parse_date(date)

    def parse_date(self, date):
        """Parse `date`.

        Parameters
        ==========
        date : string
            Date string to parse

        Returns
        =======
        N/A

        """
        # Single year: convert to integer and fill in other metadata
        try:
            self.year = int(date)
            self.period = 1
            self.freq = 1
            self.freq_id = 'A'
        # Otherwise, parse information by field
        except:
            # Apply regular expression
            pattern = re.compile(
                r'''
                (\d+)       # Year: One or more digits
                ([A-Z]+)    # Periodicity: Characters
                (\d+)       # Period: One or more digits
                ''',
                re.VERBOSE)
            match = pattern.match(date)
            # Split out fields
            self.year, self.freq_id, self.period = match.groups()
            # Convert year and period to integers
            self.year = int(self.year)
            self.period = int(self.period)
            # Identify number of periods from `freq_map`
            try:
                self.freq = self.freq_map[self.freq_id]
            except:
                raise ValueError(
                    'Unrecognised period identifier: \'%s\'' %
                    self.freq_id)

    def to_datetime(self):
        """Return the date information as a `datetime` object.

        Returns
        =======
        dt : datetime object
            Original date information as a datetime object

        """
        # Convert period information to the first month of that period
        months_in_period = 12 / self.freq
        first_month = 1 + (months_in_period * (self.period - 1))
        first_month = int(first_month)
        # Create datetime object and return
        dt = datetime.datetime(self.year, first_month, 1)
        return dt


def make_index(start, end=None, periods=None):
    """Return a pandas DatetimeIndex object from the arguments.

    Parameters
    ==========
    start : string
        Start period of the index e.g. '2000Q1'

    One of (`periods` takes precedence):
        end : string
            End period of the index, following a similar form to `start`
            e.g. '2005Q4'
        periods : integer
            Alternative to supplying an end period: the number of periods in
            the index e.g. 20

    Returns
    =======
    index : pandas DatetimeIndex object
        Index to use to construct Series objects for modelling

    """
    # Raise error if insufficient number of arguments
    if end is None and periods is None:
        raise ValueError(
            'Insufficient arguments: '
            'Must supply either an `end` period or '
            'an integer number of `periods`')
    # `periods` argument takes precedence, consistent with pandas default
    start = DateParser(start)
    if periods is not None:
        index = DatetimeIndex(
            start=start.to_datetime(),
            periods=periods,
            freq=start.freq_id)
    else:
        end = DateParser(end)
        if start.freq_id != end.freq_id:
            raise ValueError('Frequency of start and end periods differs')
        index = DatetimeIndex(
            start=start.to_datetime(),
            end=end.to_datetime(),
            freq=start.freq_id)
    # Return
    return index
