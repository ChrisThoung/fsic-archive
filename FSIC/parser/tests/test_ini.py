# -*- coding: utf-8 -*-
"""
test_ini
========
Example descriptors cite Model SIM, from Chapter 3 of Godley and Lavoie (2007).

"""


import configparser

import FSIC.parser.ini


def test_with_prefix_no_change():
    ini = '\n'.join([
        '[DEFAULT]',
        'NAME = SIM',
        'DESCRIPTION = The simplest model with government money', ])
    assert FSIC.parser.ini.with_prefix(ini) == ini


def test_with_prefix_change():
    ini = '\n'.join([
        'NAME = SIM',
        'DESCRIPTION = The simplest model with government money', ])
    assert FSIC.parser.ini.with_prefix(ini) == '[DEFAULT]\n' + ini


def test_read_string():
    ini = '\n'.join([
        '[DEFAULT]',
        'NAME = SIM',
        'DESCRIPTION = The simplest model with government money', ])
    cfg = configparser.ConfigParser()
    cfg['DEFAULT'] = {
        'NAME': 'SIM',
        'DESCRIPTION': 'The simplest model with government money'}
    assert FSIC.parser.ini.read_string(ini) == cfg


if __name__ == '__main__':
    import nose
    nose.runmodule()
