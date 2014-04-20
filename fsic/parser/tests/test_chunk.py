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


def test_parse_attributes_block():
    block = '#consumption .python .postkeynesian type="not hydraulic"'
    expected = {
        'identifier': 'consumption',
        'classes': ['python', 'postkeynesian'],
        'type': 'not hydraulic',
        }
    attributes = fsic.parser.chunk.parse_attributes_block(block)
    assert attributes == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
