# -*- coding: utf-8 -*-
"""
___NAME___
___MODULE_DOCSTRING___

"""


from fsic.model.model import Model


try:
    from IPython import get_ipython
except:
    def get_ipython():
        return None


class ___MODEL___(Model):
    """___SHORT_DESCRIPTION___

    ___LONG_DESCRIPTION___

    """

    def solve_equations(self, period):
        ___SOLVE_EQUATIONS___


if __name__ == '__main__' and get_ipython() == None:
    pass
