# -*- coding: utf-8 -*-


import fsic.parser.markdown


def test_extract_single():
    script = '\n'.join([
        '~~~{#ordinary .python}',
        'C_s = C_d',
        'G_s = G_d',
        'T_s = T_d',
        'N_s = N_d',
        '~~~'])
    chunk = fsic.parser.markdown.extract(script)
    assert chunk == [script]


if __name__ == '__main__':
    import nose
    nose.runmodule()
