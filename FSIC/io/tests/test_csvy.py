# -*- coding: utf-8 -*-
"""
test_csvy
=========
Test FSIC I/O module for files with CSV data, possibly with YAML frontmatter.

"""

from io import StringIO

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

import nose
import FSIC.io.csvy as csvy


def test_read_csv():
    data = '''\
First,Second,Third
a,1,one
b,2,two
c,3,three
'''
    xp = DataFrame({'First': ['a', 'b', 'c'],
                    'Second': [1, 2, 3],
                    'Third': ['one', 'two', 'three']})
    df = csvy.read_csvy(StringIO(data))
    assert_frame_equal(df, xp.reindex(columns=df.columns))

def test_read_csvy():
    data = '''\
---
title: Test CSV file with YAML frontmatter
variables:
 - name: First
   description: Column 1
 - name: Second
   description: Column 2
 - name: Third
   description: Column 3
---
First,Second,Third
a,1,one
b,2,two
c,3,three
'''
    xp_df = DataFrame({'First': ['a', 'b', 'c'],
                       'Second': [1, 2, 3],
                       'Third': ['one', 'two', 'three']})
    xp_fm = {'title': 'Test CSV file with YAML frontmatter',
             'variables': [{'name': 'First', 'description': 'Column 1'},
                           {'name': 'Second', 'description': 'Column 2'},
                           {'name': 'Third', 'description': 'Column 3'}]}

    df = csvy.read_csvy(StringIO(data))
    assert_frame_equal(df, xp_df.reindex(columns=df.columns))

    df, fm = csvy.read_csvy(StringIO(data), return_frontmatter=True)
    assert_frame_equal(df, xp_df.reindex(columns=df.columns))
    assert fm == xp_fm


if __name__ == '__main__':
    nose.runmodule()
