# -*- coding: utf-8 -*-


import fsic.utilities.string


def test_indent_lines():
    assert fsic.utilities.string.indent_lines(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',])) == (
    '    C_s = C_d\n    G_s = G_d\n    T_s = T_d\n    N_s = N_d')

def test_indent_lines_multiple_tabs():
    assert fsic.utilities.string.indent_lines(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), num_tabs=2) == (
    '        C_s = C_d\n        G_s = G_d\n        T_s = T_d\n        N_s = N_d')

def test_indent_lines_skip_first_line():
    assert fsic.utilities.string.indent_lines(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), skip_first_line=True) == (
    'C_s = C_d\n    G_s = G_d\n    T_s = T_d\n    N_s = N_d')

def test_indent_lines_keep_tabs():
    assert fsic.utilities.string.indent_lines(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), expand_tabs=False) == (
    '\tC_s = C_d\n\tG_s = G_d\n\tT_s = T_d\n\tN_s = N_d')

def test_indent_lines_change_tab_size():
    assert fsic.utilities.string.indent_lines(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), tab_size=2) == (
    '  C_s = C_d\n  G_s = G_d\n  T_s = T_d\n  N_s = N_d')

def test_wrap_text():
    sentences = '''Each of these sentences is longer than 80 characters and, as such, they require wrapping.
If the test function works correctly, then this text should span more lines, but each line will be 80 characters in length.'''
    expected = '''Each of these sentences is longer than 80 characters and, as such, they require
wrapping.
If the test function works correctly, then this text should span more lines, but
each line will be 80 characters in length.'''
    assert fsic.utilities.string.wrap_text(sentences) == expected

def test_wrap_text_longer():
    sentence = 'ThisSentenceHasNoDelimitingSpacesAndWillHaveToBeSplitByCharacterOnlyBecauseItIsNotObviousWhereTheWordsBeginAndEnd'
    expected = '''ThisSentenceHasNoDelimitingSpacesAndWillHaveToBeSplitByCharacterOnlyBecauseItIsN
otObviousWhereTheWordsBeginAndEnd'''
    assert fsic.utilities.string.wrap_text(sentence) == expected

def test_wrap_text_unchanged():
    no_change = 'This text is less than 80 characters and should be unchanged'
    assert fsic.utilities.string.wrap_text(no_change) == no_change

def test_wrap_text_unchanged_exact():
    no_change = 'This string is exactly 80 characters long; wrap_text() should leave it unchanged'
    assert fsic.utilities.string.wrap_text(no_change) == no_change

if __name__ == '__main__':
    import nose
    nose.runmodule()
