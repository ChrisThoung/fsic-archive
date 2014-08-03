# -*- coding: utf-8 -*-


import fsic.parser.ini


def test_with_prefix_no_change():
    ini = '\n'.join([
        '[DEFAULT]',
        'NAME = SIM',
        'DESCRIPTION = The simplest model with government money',])
    assert fsic.parser.ini.with_prefix(ini) == ini


def test_with_prefix_change():
    ini = '\n'.join([
        'NAME = SIM',
        'DESCRIPTION = The simplest model with government money',])
    assert fsic.parser.ini.with_prefix(ini) == '[DEFAULT]\n' + ini


if __name__ == '__main__':
    import nose
    nose.runmodule()
