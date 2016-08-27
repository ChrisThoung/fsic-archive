# -*- coding: utf-8 -*-
"""
test_parser
===========
Test FSIC Markdown parser and wrappers.

"""

import os

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

import nose

from FSIC.classes.equation import Equation
from FSIC.parser.markdown import read_markdown
from FSIC.parser.wrappers import read_python


def test_read_markdown_empty():
    assert read_markdown('') is None

def test_read_python_empty():
    assert read_python('') is None


def test_read_markdown():
    data = '''\
---
---

```{#Consumption .python function='consumption'}
C_d = {alpha_1} * YD + {alpha_2} * H_h[-1] + <epsilon>
```

```{#Stocks .python type=accounting}
H_h = H_h[-1] + YD - C_d
```

```{#Hidden .python .hidden}
H_h = H_s
```

'''
    xp_block_table = DataFrame.from_dict({
        '_Frontmatter': {'_raw': '',
                         '.yaml': True, '.python': False, '.hidden': False,
                         'function': '', 'type': ''},
        'Consumption': {'_raw': 'C_d = {alpha_1} * YD + {alpha_2} * H_h[-1] + <epsilon>',
                        '.yaml': False, '.python': True, '.hidden': False,
                        'function': 'consumption', 'type': ''},
        'Stocks': {'_raw': 'H_h = H_h[-1] + YD - C_d',
                   '.yaml': False, '.python': True, '.hidden': False,
                   'function': '', 'type': 'accounting'},
        'Hidden': {'_raw': 'H_h = H_s',
                   '.yaml': False, '.python': True, '.hidden': True,
                   'function': '', 'type': ''}},
                                   orient='index')
    xp_equation_table = DataFrame.from_dict({
        'C_d = alpha_1 * YD + alpha_2 * H_h[-1] + epsilon': {'block': 'Consumption'},
        'H_h = H_h[-1] + YD - C_d': {'block': 'Stocks'}},
                                   orient='index')
    xp_equations = [Equation(x)
                    for x in ['C_d[0] = {alpha_1} * YD + {alpha_2} * H_h[-1] + <epsilon>',
                              'H_h[0] = H_h[-1] + YD[0] - C_d[0]',
                              'H_h = H_s']]
    xp_symbol_table = DataFrame.from_dict({
        'C_d': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'C_d = alpha_1 * YD + alpha_2 * H_h[-1] + epsilon'},
        'alpha_1': {'type': 'parameter', 'min': 0, 'max': 0, 'equation': ''},
        'YD': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''},
        'alpha_2': {'type': 'parameter', 'min': 0, 'max': 0, 'equation': ''},
        'H_h': {'type': 'endogenous', 'min': -1, 'max': 0, 'equation': 'H_h = H_h[-1] + YD - C_d'},
        'epsilon': {'type': 'error', 'min': 0, 'max': 0, 'equation': ''}},
                                   orient='index')

    schematic = read_markdown(data)

    assert_frame_equal(
        schematic.block_table,
        xp_block_table.reindex(index=schematic.block_table.index,
                               columns=schematic.block_table.columns))
    for e, x in zip(schematic.equations.values(), xp_equations):
        assert e == x
    assert_frame_equal(
        schematic.equation_table.reindex(
            index=xp_equation_table.index,
            columns=xp_equation_table.columns),
        xp_equation_table)
    assert_frame_equal(
        schematic.symbol_table.reindex(
            index=xp_symbol_table.index,
            columns=xp_symbol_table.columns),
        xp_symbol_table)


def check_python(schematic):
    xp_block_table = DataFrame.from_dict({
        '_Frontmatter': {'_raw': '', '.yaml': True, '.python': False},
        'Python': {'_raw': 'C_s = C_d\nG_s = G_d\nT_s = T_d\nN_s = N_d # No labour supply constraints\n',
                            '.yaml': False, '.python': True}},
                                   orient='index')
    xp_equation_table = DataFrame.from_dict({
        'C_s = C_d': {'block': 'Python'},
        'G_s = G_d': {'block': 'Python'},
        'T_s = T_d': {'block': 'Python'},
        'N_s = N_d': {'block': 'Python'}},
                                   orient='index')
    xp_equations = [Equation(x)
                    for x in ['C_s = C_d', 'G_s = G_d',
                              'T_s = T_d', 'N_s = N_d']]
    xp_symbol_table = DataFrame.from_dict({
        'C_s': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'C_s = C_d'},
        'C_d': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''},
        'G_s': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'G_s = G_d'},
        'G_d': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''},
        'T_s': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'T_s = T_d'},
        'T_d': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''},
        'N_s': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'N_s = N_d'},
        'N_d': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''}},
                                   orient='index')
    assert_frame_equal(
        schematic.block_table,
        xp_block_table.reindex(index=schematic.block_table.index,
                               columns=schematic.block_table.columns))
    for e, x in zip(schematic.equations.values(), xp_equations):
        assert e == x
    assert_frame_equal(
        schematic.equation_table.reindex(
            index=xp_equation_table.index,
            columns=xp_equation_table.columns),
        xp_equation_table)
    assert_frame_equal(
        schematic.symbol_table.reindex(
            index=xp_symbol_table.index,
            columns=xp_symbol_table.columns),
        xp_symbol_table)

def test_read_python():
    data = '''\
C_s = C_d
G_s = G_d
T_s = T_d
N_s = N_d # No labour supply constraints
'''
    schematic = read_python(data)
    check_python(schematic)

def test_read_python_from_file():
    schematic = read_python(os.path.join(os.path.split(__file__)[0],
                                         'data',
                                         'python.txt'))
    check_python(schematic)


if __name__ == '__main__':
    nose.runmodule()
