# -*- coding: utf-8 -*-
"""
test_exec
=========
Test FSIC CLI handling of user commands.

"""

from fsic.cli.model import translate

import nose


def test_translate():
    cases = [
        ('G=20','model.G = 20'),
        ('G=20.','model.G = 20.'),
        ('G=20.0','model.G = 20.0'),
        ('G[1:]=20','model.G[1:] = 20'),

        ('alpha_2=0.4','model.alpha_2 = 0.4'),
        ('alpha_2=.4','model.alpha_2 = .4'),

        ("G['2000'] = 20", "model.G['2000'] = 20"),
        ("G['2000Q1':] = 20", "model.G['2000Q1':] = 20"),

        ('C=ABJR+HAYO', 'model.C = model.ABJR + model.HAYO'),
    ]
    for (input_, expected) in cases:
        output = translate(input_)
        assert output == expected


if __name__ == '__main__':
    nose.runmodule()
