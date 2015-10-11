# -*- coding: utf-8 -*-


import re

import networkx.algorithms.isomorphism as iso
import networkx as nx

from FSIC.classes.schematic import Equation


def test_init_parse_default():
    eqn = Equation('C_d = alpha_1 * YD + alpha_2 * H_h[-1]')
    assert eqn.n == ['C_d']
    assert eqn.x == ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]']
    assert eqn.vars == ('C_d', 'alpha_1', 'YD', 'alpha_2', 'H_h[-1]')
    assert eqn.expr == '%s = %s * %s + %s * %s'
    assert eqn.count == 5
    assert eqn.string == eqn.expr % eqn.vars

def test_init_parse_sep():
    eqn = Equation('C_d : alpha_1, YD, alpha_2, H_h[-1]',
                   sep=':')
    assert eqn.n == ['C_d']
    assert eqn.x == ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]']
    assert eqn.vars == ('C_d', 'alpha_1', 'YD', 'alpha_2', 'H_h[-1]')
    assert eqn.expr == '%s : %s, %s, %s, %s'
    assert eqn.count == 5
    assert eqn.string == eqn.expr % eqn.vars

def test_init_parse_regex():
    eqn = Equation('C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
                   regex=re.compile(r'\b[A-Z][_0-z]+\b'))
    assert eqn.n == ['C_d']
    assert eqn.x == ['YD', 'H_h']
    assert eqn.vars == ('C_d', 'YD', 'H_h')
    assert eqn.expr == '%s = alpha_1 * %s + alpha_2 * %s[-1]'
    assert eqn.count == 3
    assert eqn.string == eqn.expr % eqn.vars

def test_init_parse_both():
    eqn = Equation('C_d : alpha_1, YD, alpha_2, H_h[-1]',
                   sep=':',
                   regex=re.compile(r'\b[A-Z][_0-z]+\b'))
    assert eqn.n == ['C_d']
    assert eqn.x == ['YD', 'H_h']
    assert eqn.vars == ('C_d', 'YD', 'H_h')
    assert eqn.expr == '%s : alpha_1, %s, alpha_2, %s[-1]'
    assert eqn.count == 3
    assert eqn.string == eqn.expr % eqn.vars


def test_parse_string_arg_default():
    eqn = Equation()
    eqn.parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]')
    assert eqn.n == ['C_d']
    assert eqn.x == ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]']
    assert eqn.vars == ('C_d', 'alpha_1', 'YD', 'alpha_2', 'H_h[-1]')
    assert eqn.expr == '%s = %s * %s + %s * %s'
    assert eqn.count == 5
    assert eqn.string == eqn.expr % eqn.vars

def test_parse_string_arg_sep_str():
    eqn = Equation()
    eqn.parse('C_d : alpha_1, YD, alpha_2, H_h[-1]',
              sep=':')
    assert eqn.n == ['C_d']
    assert eqn.x == ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]']
    assert eqn.vars == ('C_d', 'alpha_1', 'YD', 'alpha_2', 'H_h[-1]')
    assert eqn.expr == '%s : %s, %s, %s, %s'
    assert eqn.count == 5
    assert eqn.string == eqn.expr % eqn.vars

def test_parse_string_arg_sep_re():
    eqn = Equation()
    eqn.parse('C_d : alpha_1, YD, alpha_2, H_h[-1]',
              sep=re.compile(r':'))
    assert eqn.n == ['C_d']
    assert eqn.x == ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]']
    assert eqn.vars == ('C_d', 'alpha_1', 'YD', 'alpha_2', 'H_h[-1]')
    assert eqn.expr == '%s : %s, %s, %s, %s'
    assert eqn.count == 5
    assert eqn.string == eqn.expr % eqn.vars

def test_parse_string_arg_regex_str():
    eqn = Equation()
    eqn.parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
              regex=r'\b[A-Z][_0-z]+\b')
    assert eqn.n == ['C_d']
    assert eqn.x == ['YD', 'H_h']
    assert eqn.vars == ('C_d', 'YD', 'H_h')
    assert eqn.expr == '%s = alpha_1 * %s + alpha_2 * %s[-1]'
    assert eqn.count == 3
    assert eqn.string == eqn.expr % eqn.vars

def test_parse_string_arg_regex_re():
    eqn = Equation()
    eqn.parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
              regex=re.compile(r'\b[A-Z][_0-z]+\b'))
    assert eqn.n == ['C_d']
    assert eqn.x == ['YD', 'H_h']
    assert eqn.vars == ('C_d', 'YD', 'H_h')
    assert eqn.expr == '%s = alpha_1 * %s + alpha_2 * %s[-1]'
    assert eqn.count == 3
    assert eqn.string == eqn.expr % eqn.vars

def test_to_graph_consumption():
    eqn = Equation('C_d = alpha_1 * YD + alpha_2 * H_h[-1]')

    expected = nx.DiGraph()
    expected.add_node(
        'C_d[period]',
        equation='C_d[period] = alpha_1[period] * YD[period] + alpha_2[period] * H_h[period-1]')
    for x in ['alpha_1[period]', 'YD[period]', 'alpha_2[period]', 'H_h[period-1]']:
        expected.add_edge(x, 'C_d[period]')

    G = eqn.to_graph()

    nm = iso.categorical_node_match('equation', '')
    assert nx.is_isomorphic(G, expected, node_match=nm)


if __name__ == '__main__':
    import nose
    nose.runmodule()
