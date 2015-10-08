# -*- coding: utf-8 -*-


from FSIC.classes import Variable


def test_parse_current_no_index():
    var = Variable()
    var.parse('C_d')
    assert var.name == 'C_d'
    assert var.index == None
    assert var.mindex == '[period]'
    assert var.expr == 'C_d[period]'

def test_parse_current_zero_index():
    var = Variable()
    var.parse('C_d[0]')
    assert var.name == 'C_d'
    assert var.index == '[0]'
    assert var.mindex == '[period]'
    assert var.expr == 'C_d[period]'

def test_parse_current_empty_index():
    var = Variable()
    var.parse('C_d[]')
    assert var.name == 'C_d'
    assert var.index == '[]'
    assert var.mindex == '[period]'
    assert var.expr == 'C_d[period]'

def test_parse_lag():
    var = Variable()
    var.parse('H_h[-1]')
    assert var.name == 'H_h'
    assert var.index == '[-1]'
    assert var.mindex == '[period-1]'
    assert var.expr == 'H_h[period-1]'

def test_parse_lead():
    var = Variable()
    var.parse('YD[1]')
    assert var.name == 'YD'
    assert var.index == '[1]'
    assert var.mindex == '[period+1]'
    assert var.expr == 'YD[period+1]'

def test_parse_lead_signed():
    var = Variable()
    var.parse('YD[+1]')
    assert var.name == 'YD'
    assert var.index == '[+1]'
    assert var.mindex == '[period+1]'
    assert var.expr == 'YD[period+1]'


if __name__ == '__main__':
    import nose
    nose.runmodule()
