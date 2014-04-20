# -*- coding: utf-8 -*-


import fsic.parser.chunk


def test_split():
    chunk = '\n'.join([
        '~~~{#ordinary .python}',
        'C_s = C_d',
        'G_s = G_d',
        'T_s = T_d',
        'N_s = N_d',
        '~~~'])
    contents = fsic.parser.chunk.split(chunk)
    assert contents == {
        'attributes': '#ordinary .python',
        'code': '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',])
        }


if __name__ == '__main__':
    import nose
    nose.runmodule()
