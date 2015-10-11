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

    expected.add_node('C_s[0]', equations=['C_s[0] = C_d[0]'], functions=['Accounting'])
    expected.add_node('G_s[0]', equations=['G_s[0] = G_d[0]'], functions=['Accounting'])
    expected.add_node('T_s[0]', equations=['T_s[0] = T_d[0]'], functions=['Accounting'])
    expected.add_node('N_s[0]', equations=['N_s[0] = N_d[0]'], functions=['Accounting'])
    expected.add_node('YD[0]', equations=['YD[0] = W[0] * N_s[0] - T_s[0]'], functions=['Disposable income and taxes'])
    expected.add_node('T_d[0]', equations=['T_d[0] = theta[0] * W[0] * N_s[0]'], functions=['Disposable income and taxes'])
    expected.add_node('C_d[0]', equations=['C_d[0] = alpha_1[0] * YD[0] + alpha_2[0] * H_h[-1]'], functions=['Consumption'])
    expected.add_node('H_s[0]', equations=['H_s[0] = H_s[-1] + G_d[0] - T_d[0]'], functions=['Stocks'])
    expected.add_node('H_h[0]', equations=['H_h[0] = H_h[-1] + YD[0] - C_d[0]'], functions=['Stocks'])
    expected.add_node('Y[0]', equations=['Y[0] = C_s[0] + G_s[0]'], functions=['(National) income'])
    expected.add_node('N_d[0]', equations=['N_d[0] = Y[0] / W[0]'], functions=['(National) income'])

    expected.add_edge('C_d[0]', 'C_s[0]')
    expected.add_edge('G_d[0]', 'G_s[0]')
    expected.add_edge('T_d[0]', 'T_s[0]')
    expected.add_edge('N_d[0]', 'N_s[0]')
    expected.add_edge('W[0]', 'YD[0]')
    expected.add_edge('N_s[0]', 'YD[0]')
    expected.add_edge('T_s[0]', 'YD[0]')
    expected.add_edge('theta[0]', 'T_d[0]')
    expected.add_edge('W[0]', 'T_d[0]')
    expected.add_edge('N_s[0]', 'T_d[0]')
    expected.add_edge('alpha_1[0]', 'C_d[0]')
    expected.add_edge('YD[0]', 'C_d[0]')
    expected.add_edge('alpha_2[0]', 'C_d[0]')
    expected.add_edge('H_h[-1]', 'C_d[0]')
    expected.add_edge('H_s[-1]', 'H_s[0]')
    expected.add_edge('G_d[0]', 'H_s[0]')
    expected.add_edge('T_d[0]', 'H_s[0]')
    expected.add_edge('H_h[-1]', 'H_h[0]')
    expected.add_edge('YD[0]', 'H_h[0]')
    expected.add_edge('C_d[0]', 'H_h[0]')
    expected.add_edge('C_s[0]', 'Y[0]')
    expected.add_edge('G_s[0]', 'Y[0]')
    expected.add_edge('Y[0]', 'N_d[0]')
    expected.add_edge('W[0]', 'N_d[0]')

    assert nx.is_isomorphic(G, expected, node_match=dict.__eq__)


if __name__ == '__main__':
    import nose
    nose.runmodule()
