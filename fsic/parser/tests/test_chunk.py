# -*- coding: utf-8 -*-


from nose.tools import raises
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


def test_parse_attributes_block_identifier():
    identifier = fsic.parser.chunk.parse_attributes_block_identifier(
        '#consumption')
    assert identifier == 'consumption'


def test_parse_attributes_block_identifier_empty():
    identifier = fsic.parser.chunk.parse_attributes_block_identifier('')
    assert identifier == None


def test_parse_attributes_block_classes():
    classes = fsic.parser.chunk.parse_attributes_block_classes(
        '.python .postkeynesian')
    assert classes == ['python', 'postkeynesian']


def test_parse_attributes_block_classes_empty():
    classes = fsic.parser.chunk.parse_attributes_block_classes('')
    assert classes == []


def test_parse_attributes_block_attributes():
    attributes = fsic.parser.chunk.parse_attributes_block_attributes(
        'type="not hydraulic"')
    assert attributes == {
        'type': 'not hydraulic'}


def test_parse_attributes_block_attributes_empty():
    attributes = fsic.parser.chunk.parse_attributes_block_attributes('')
    assert attributes == {}


@raises(ValueError)
def test_parse_attributes_block_attributes_duplicates():
    attributes = fsic.parser.chunk.parse_attributes_block_attributes(
        'type="not hydraulic" type="hydraulic"')


def test_parse_attributes_block():
    block = '#consumption .python .postkeynesian type="not hydraulic"'
    expected = {
        'identifier': 'consumption',
        'classes': ['python', 'postkeynesian'],
        'type': 'not hydraulic',
        }
    attributes = fsic.parser.chunk.parse_attributes_block(block)
    assert attributes == expected


def test_parse_attributes_block_empty():
    block = ''
    expected = {
        'identifier': None,
        'classes': [],
        }
    attributes = fsic.parser.chunk.parse_attributes_block(block)
    assert attributes == expected


if __name__ == '__main__':
    import nose
    nose.runmodule()
