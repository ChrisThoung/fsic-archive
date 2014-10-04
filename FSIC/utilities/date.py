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
                ([AQM])     # Periodicity: One character
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
            self.freq = self.freq_map[self.freq_id]

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
