# -*- coding: utf-8 -*-


import networkx.algorithms.isomorphism as iso
import networkx as nx

from FSIC.classes.schematic import Model


def test_to_graph():
    m = Model()
    m.add_function(['C_s = C_d',
                    'G_s = G_d',
                    'T_s = T_d',
                    'N_s = N_d', ],
                   'Accounting')
    m.add_function(['YD = W * N_s - T_s',
                    'T_d = theta * W * N_s', ],
                   'Disposable income and taxes')
    m.add_function(['C_d = alpha_1 * YD + alpha_2 * H_h[-1]', ],
                   'Consumption')
    m.add_function(['H_s = H_s[-1] + G_d - T_d',
                    'H_h = H_h[-1] + YD - C_d', ],
                   'Stocks')
    m.add_function(['Y = C_s + G_s',
                    'N_d = Y / W', ],
                   '(National) income')
    G = m.to_graph()

    expected = nx.DiGraph()

    expected.add_node('C_s[period]', equations=['C_s[period] = C_d[period]'], functions=['Accounting'])
    expected.add_node('G_s[period]', equations=['G_s[period] = G_d[period]'], functions=['Accounting'])
    expected.add_node('T_s[period]', equations=['T_s[period] = T_d[period]'], functions=['Accounting'])
    expected.add_node('N_s[period]', equations=['N_s[period] = N_d[period]'], functions=['Accounting'])
    expected.add_node('YD[period]', equations=['YD[period] = W[period] * N_s[period] - T_s[period]'], functions=['Disposable income and taxes'])
    expected.add_node('T_d[period]', equations=['T_d[period] = theta[period] * W[period] * N_s[period]'], functions=['Disposable income and taxes'])
    expected.add_node('C_d[period]', equations=['C_d[period] = alpha_1[period] * YD[period] + alpha_2[period] * H_h[period-1]'], functions=['Consumption'])
    expected.add_node('H_s[period]', equations=['H_s[period] = H_s[period-1] + G_d[period] - T_d[period]'], functions=['Stocks'])
    expected.add_node('H_h[period]', equations=['H_h[period] = H_h[period-1] + YD[period] - C_d[period]'], functions=['Stocks'])
    expected.add_node('Y[period]', equations=['Y[period] = C_s[period] + G_s[period]'], functions=['(National) income'])
    expected.add_node('N_d[period]', equations=['N_d[period] = Y[period] / W[period]'], functions=['(National) income'])

    expected.add_edge('C_d[period]', 'C_s[period]')
    expected.add_edge('G_d[period]', 'G_s[period]')
    expected.add_edge('T_d[period]', 'T_s[period]')
    expected.add_edge('N_d[period]', 'N_s[period]')
    expected.add_edge('W[period]', 'YD[period]')
    expected.add_edge('N_s[period]', 'YD[period]')
    expected.add_edge('T_s[period]', 'YD[period]')
    expected.add_edge('theta[period]', 'T_d[period]')
    expected.add_edge('W[period]', 'T_d[period]')
    expected.add_edge('N_s[period]', 'T_d[period]')
    expected.add_edge('alpha_1[period]', 'C_d[period]')
    expected.add_edge('YD[period]', 'C_d[period]')
    expected.add_edge('alpha_2[period]', 'C_d[period]')
    expected.add_edge('H_h[period-1]', 'C_d[period]')
    expected.add_edge('H_s[period-1]', 'H_s[period]')
    expected.add_edge('G_d[period]', 'H_s[period]')
    expected.add_edge('T_d[period]', 'H_s[period]')
    expected.add_edge('H_h[period-1]', 'H_h[period]')
    expected.add_edge('YD[period]', 'H_h[period]')
    expected.add_edge('C_d[period]', 'H_h[period]')
    expected.add_edge('C_s[period]', 'Y[period]')
    expected.add_edge('G_s[period]', 'Y[period]')
    expected.add_edge('Y[period]', 'N_d[period]')
    expected.add_edge('W[period]', 'N_d[period]')

    assert nx.is_isomorphic(G, expected, node_match=dict.__eq__)


if __name__ == '__main__':
    import nose
    nose.runmodule()
