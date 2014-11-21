.. _example-run:

***********************************************
Simulating Godley and Lavoie's (2007) Model SIM
***********************************************

This section is the second part of the example, to show how to specify Godley
and Lavoie's (2007) *Model SIM* and conduct numerical simulations.


.. _example-run-equations:

Model equations
===============


.. _example-run-equations-ds:

Equalising demand and supply
----------------------------

.. math::
   :label: sd-consumption

   C_s = C_d

.. math::
   :label: sd-government

   G_s = G_d

.. math::
   :label: sd-taxes

   T_s = T_d

.. math::
   :label: sd-labour

   N_s = N_d


.. _example-run-equations-income:

Disposable income
-----------------

.. math::
   :label: income

   YD = W . N_s - T_s

.. math::
   :label: taxation

   T_d = \theta . W. N_s \qquad \theta < 1

.. |theta| replace:: :math:`\theta`


.. _example-run-equations-consumption:

Consumption function
--------------------

.. math::
   :label: consumption

   C_d = \alpha _1 . YD + \alpha _2 . H_{h-1} \qquad 0 < \alpha _1 < \alpha _2 < 1

.. |H[-1]| replace:: :math:`H_{-1}`


.. _example-run-balances:

Financial balances
------------------

.. math::
   :label: government-debt

   \Delta H_s = H_s - H_{s-1} = G_d - T_d

.. |H_s| replace:: :math:`H_s`

.. math::
   :label: household-wealth

   \Delta H_h = H_h - H_{h-1} = YD - C_d


.. _example-run-output-employment:

Output and employment
---------------------

.. math::
   :label: output

   Y = C_s + G_s

.. math::
   :label: labour

   N_d = \frac{Y}{W}


.. _example-run-redundant:

The redundant equation
----------------------

.. math::
   \Delta H_h = \Delta H_s
