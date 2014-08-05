# -*- coding: utf-8 -*-


import fsic.utilities.string


def test_indent():
    assert fsic.utilities.string.indent(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',])) == (
    'C_s = C_d\n    G_s = G_d\n    T_s = T_d\n    N_s = N_d')

def test_indent_multiple_tabs():
    assert fsic.utilities.string.indent(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), num_tabs=2) == (
    'C_s = C_d\n        G_s = G_d\n        T_s = T_d\n        N_s = N_d')

def test_indent_including_first_line():
    assert fsic.utilities.string.indent(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), include_first_line=True) == (
    '    C_s = C_d\n    G_s = G_d\n    T_s = T_d\n    N_s = N_d')

def test_indent_keep_tabs():
    assert fsic.utilities.string.indent(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), spaces_instead_of_tabs=False) == (
    'C_s = C_d\n\tG_s = G_d\n\tT_s = T_d\n\tN_s = N_d')

def test_indent_different_number_of_spaces():
    assert fsic.utilities.string.indent(
        '\n'.join([
            'C_s = C_d',
            'G_s = G_d',
            'T_s = T_d',
            'N_s = N_d',]), spaces_to_tabs=2) == (
    'C_s = C_d\n  G_s = G_d\n  T_s = T_d\n  N_s = N_d')


if __name__ == '__main__':
    import nose
    nose.runmodule()
