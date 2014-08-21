# -*- coding: utf-8 -*-


import fsic.optimise.order


def test_recursive():
    equations = [
        'self.H_h[period] = self.H_s[period]',
        'self.C_d[period] = self.alpha_1[period] * self.YD[period] + self.alpha_2[period] * self.H_h[period-1]',
        'self.C_s[period] = self.C_d[period]',
        'self.G_s[period] = self.G_d[period]',
        'self.T_s[period] = self.T_d[period]',
        'self.N_s[period] = self.N_d[period]',
        'self.H_s[period] = self.H_s[period-1] + self.G_d[period] - self.T_d[period]',
        'self.H_h[period] = self.H_h[period-1] + self.YD[period] - self.C_d[period]',
        'self.Y[period] = self.C_s[period] + self.G_s[period]',
        'self.N_d[period] = self.Y[period] / self.W[period]',
        'self.YD[period] = self.W[period] * self.N_s[period] - self.T_s[period]',
        'self.T_d[period] = self.theta[period] * self.W[period] * self.N_s[period]',
    ]
    reordered = []
    assert fsic.optimise.order.recursive(equations) == reordered


if __name__ == '__main__':
    import nose
    nose.runmodule()
