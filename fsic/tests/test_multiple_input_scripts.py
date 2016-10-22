# -*- coding: utf-8 -*-
"""
test_multiple_input_scripts
===========================
Test FSIC components to read and join multiple input scripts into a single
`Schematic` object.

"""

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from fsic.classes.equation import Equation
from fsic.classes.schematic import Schematic
from fsic.parser.wrappers import read_markdown, read_python


def test_schematic_merge_two():
    s1 = read_python('C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]')
    s2 = read_python('H_h = H_h[-1] + YD - C_d')
    merged = Schematic.merge([s1, s2])

    xp_block_table = DataFrame.from_dict({
        '_Frontmatter': {'_raw': '',
                         '.yaml': True, '.python': False},
        'Python_0': {'_raw': 'C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]',
                     '.yaml': False, '.python': True},
        'Python_1': {'_raw': 'H_h = H_h[-1] + YD - C_d',
                     '.yaml': False, '.python': True}, },
                                         orient='index')
    assert_frame_equal(
        merged.block_table.reindex(index=xp_block_table.index,
                                   columns=xp_block_table.columns),
        xp_block_table)

    xp_equation_table = DataFrame.from_dict({
        'C_d = alpha_1 * YD + alpha_2 * H_h[-1]': {'block': 'Python_0'},
        'H_h = H_h[-1] + YD - C_d': {'block': 'Python_1'}},
                                            orient='index')
    assert_frame_equal(
        merged.equation_table.reindex(index=xp_equation_table.index,
                                      columns=xp_equation_table.columns),
        xp_equation_table)

    xp_equations = [Equation(x)
                    for x in ['C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]',
                              'H_h = H_h[-1] + YD - C_d', ]]
    for e, x in zip(merged.equations.values(), xp_equations):
        assert e == x

    xp_symbol_table = DataFrame.from_dict({
        'C_d': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'C_d = alpha_1 * YD + alpha_2 * H_h[-1]'},
        'alpha_1': {'type': 'parameter', 'min': 0, 'max': 0, 'equation': ''},
        'YD': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''},
        'alpha_2': {'type': 'parameter', 'min': 0, 'max': 0, 'equation': ''},
        'H_h': {'type': 'endogenous', 'min': -1, 'max': 0, 'equation': 'H_h = H_h[-1] + YD - C_d'}, },
                                          orient='index')
    assert_frame_equal(
        merged.symbol_table.reindex(index=xp_symbol_table.index,
                                    columns=xp_symbol_table.columns),
        xp_symbol_table)


def test_schematic_merge_three():
    s1 = read_python('C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]')
    s2 = read_python('H_h = H_h[-1] + YD - C_d')
    s3 = read_python('C_s = C_d')
    merged = Schematic.merge([s1, s2, s3])

    xp_block_table = DataFrame.from_dict({
        '_Frontmatter': {'_raw': '',
                         '.yaml': True, '.python': False},
        'Python_0': {'_raw': 'C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]',
                     '.yaml': False, '.python': True},
        'Python_1': {'_raw': 'H_h = H_h[-1] + YD - C_d',
                     '.yaml': False, '.python': True},
        'Python': {'_raw': 'C_s = C_d',
                     '.yaml': False, '.python': True}, },
                                         orient='index')
    assert_frame_equal(
        merged.block_table.reindex(index=xp_block_table.index,
                                   columns=xp_block_table.columns),
        xp_block_table)

    xp_equation_table = DataFrame.from_dict({
        'C_d = alpha_1 * YD + alpha_2 * H_h[-1]': {'block': 'Python_0'},
        'H_h = H_h[-1] + YD - C_d': {'block': 'Python_1'},
        'C_s = C_d': {'block': 'Python'}, },
                                            orient='index')
    assert_frame_equal(
        merged.equation_table.reindex(index=xp_equation_table.index,
                                      columns=xp_equation_table.columns),
        xp_equation_table)

    xp_equations = [Equation(x)
                    for x in ['C_d = {alpha_1} * YD + {alpha_2} * H_h[-1]',
                              'H_h = H_h[-1] + YD - C_d',
                              'C_s = C_d', ]]
    for e, x in zip(merged.equations.values(), xp_equations):
        assert e == x

    xp_symbol_table = DataFrame.from_dict({
        'C_d': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'C_d = alpha_1 * YD + alpha_2 * H_h[-1]'},
        'alpha_1': {'type': 'parameter', 'min': 0, 'max': 0, 'equation': ''},
        'YD': {'type': 'exogenous', 'min': 0, 'max': 0, 'equation': ''},
        'alpha_2': {'type': 'parameter', 'min': 0, 'max': 0, 'equation': ''},
        'H_h': {'type': 'endogenous', 'min': -1, 'max': 0, 'equation': 'H_h = H_h[-1] + YD - C_d'},
        'C_s': {'type': 'endogenous', 'min': 0, 'max': 0, 'equation': 'C_s = C_d'}, },
                                          orient='index')
    assert_frame_equal(
        merged.symbol_table.reindex(index=xp_symbol_table.index,
                                    columns=xp_symbol_table.columns),
        xp_symbol_table)


def test_frontmatter_handling():
    # Check that frontmatter variables do not appear in the merged symbol table
    frontmatter = '''\
---
name: SomeModel
---
'''
    equation = '''\
```{.python}
Y = C + I + G + X - M
```
'''
    merged = Schematic.merge([read_markdown(frontmatter),
                              read_markdown(equation)])
    assert sorted(merged.symbol_table.index.tolist()) == sorted(list('YCIGXM'))


if __name__ == '__main__':
    nose.runmodule()
