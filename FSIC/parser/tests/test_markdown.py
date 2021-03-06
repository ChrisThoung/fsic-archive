# -*- coding: utf-8 -*-
"""
test_markdown
=============
Example equations come from Model SIM, from Chapter 3 of Godley and Lavoie
(2007).

"""


import FSIC.parser.markdown


def test_extract_single():
    script = '\n'.join([
        '~~~{#ordinary .python}',
        'C_s = C_d',
        'G_s = G_d',
        'T_s = T_d',
        'N_s = N_d',
        '~~~'])
    chunk = FSIC.parser.markdown.extract(script)
    assert chunk == [script]


def test_extract_multiple():
    script = '\n'.join([
        '~~~{#ordinary .python}',
        'C_s = C_d',
        'G_s = G_d',
        'T_s = T_d',
        'N_s = N_d',
        '~~~',
        '',
        '```{.python}',
        'YD = W * N_s - T_s',
        '```',
        '',
        '~~~{.python}',
        'C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
        '~~~',
        '~~~{#output .python}',
        'Y = C_s + G_s',
        '~~~'])
    expected = [
        '\n'.join([
            '~~~{#ordinary .python}',
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',
            '~~~']),
        '\n'.join([
            '```{.python}',
            'YD = W * N_s - T_s',
            '```']),
        '\n'.join([
            '~~~{.python}',
            'C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
            '~~~']),
        '\n'.join([
            '~~~{#output .python}',
            'Y = C_s + G_s',
            '~~~']),
        ]
    chunks = FSIC.parser.markdown.extract(script)
    assert chunks == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
