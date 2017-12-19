# -*- coding: utf-8 -*-
"""
test_cli_model
==============
Test FSIC model CLI.

"""

import os

import nose

from pandas import Series, PeriodIndex
from pandas.testing import assert_series_equal

import fsic


class CurrentAccount(fsic.Model):
    """Reproduce headline accounting of the UK current account using ONS
       database codes.
    """

    VARIABLES = ['KTMY', 'LQCT', 'KTMS', 'HMBP', 'KTMP', 'HMBM', 'MT5W', 'HBOG', 'KTNF']
    PARAMETERS = []
    ERRORS = []

    CONVERGENCE_VARIABLES = ['KTMY', 'HMBP', 'HBOG']

    START_OFFSET = 0
    END_OFFSET = 0

    VERSION = '0.1.0.dev'


    def _solve_python_iteration(self, row):
        self.HMBP.values[row] = self.KTMP.values[row] + self.HMBM.values[row] + self.MT5W.values[row]
        self.KTMY.values[row] = self.LQCT.values[row] + self.KTMS.values[row]
        self.HBOG.values[row] = self.KTMY.values[row] + self.HMBP.values[row] + self.KTNF.values[row]


import fsic.cli.model
parser, handle_args = fsic.cli.model.make_cli(CurrentAccount)


def test_period_args():
    # Test case where the input data file defines the model span but the user
    # specifies a different first period for solution
    expected = Series(26,
                      index=PeriodIndex(start='1994Q1', end='2000Q4'),
                      name='HBOG')

    input_data_path = os.path.join(os.path.split(__file__)[0],
                                   'data', 'pnbp_dummy.csv')
    model = handle_args(parser.parse_args(['solve',
                                           '--solve-from', '1995Q1',
                                           '-f', input_data_path]))

    assert_series_equal(model.HBOG, expected)


if __name__ == '__main__':
    nose.runmodule()
