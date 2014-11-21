.. _example:

************************************************
An example: Godley and Lavoie's (2007) Model SIM
************************************************

This section provides an example of how to generate a model from a Markdown file
and run the resulting Python script. It uses *Model SIM* from Godley and
Lavoie (2007) as an example.


.. _example-intro:

Introduction
============

*Model SIM* is the first model in Godley and Lavoie (2007). It is the *simplest*
meaningful model that can be built, with the following key features:

* A closed economy, with neither exports, imports or foreign capital flows
* Production is entirely of services, with no requirement for capital equipment
  and no intermediate costs of production
* Moreover, service production is instantaneous, obviating any requirement for
  inventories and, by extension, finance for inventory accumulation
* All transactions take place in government money such that government money is
  the vehicle for household income, debt settlement, tax payment and wealth
  storage
* There is an unlimited quantity of labour at a fixed price, such that the
  supply of labour places no constraints on production; the implication is that
  the economy is demand-led, and *not* supply-constrained


.. _example-accounts:

Accounting matrices
===================

The balance sheet for *Model SIM* consists of just one item: money, which is
printed by the government and assumed to consist entirely of banknotes. This is
*cash* or *high-powered* money. Money (*H*) is an asset of households and a
corresponding liability for the government.

.. csv-table:: The balance sheet of Model *SIM*
   :header: "", Households, Production, Government
   :stub-columns: 1
   :widths: 30, 15, 15, 15

   Money stock, |+H|, "", |-H|

.. |-H| replace:: :math:`-H`
.. |+H| replace:: :math:`+H`

The transactions matrix below sets out the flows of funds that drive changes in
the money stock from year to year.

.. csv-table:: Accounting (transactions) matrix for Model *SIM*
   :header: "", Households, Production, Government
   :stub-columns: 1
   :widths: 30, 15, 15, 15

   Consumption, |-C|, |+C|, ""
   Government expenditures, "", |+G|, |-G|
   [Output], "", |[Y]|, ""
   Factor income (wages), |+WB|, |-WB|, ""
   Taxes, |-T|, "", |+T|
   Change in the stock of money, |-D(H)|, "", |+D(H)|

.. |-C| replace:: :math:`-C`
.. |+C| replace:: :math:`+C`
.. |-G| replace:: :math:`-G`
.. |+G| replace:: :math:`+G`
.. |[Y]| replace:: :math:`[Y]`
.. |-WB| replace:: :math:`-WB`
.. |+WB| replace:: :math:`+WB`
.. |-T| replace:: :math:`-T`
.. |+T| replace:: :math:`+T`
.. |-D(H)| replace:: :math:`- \Delta H`
.. |+D(H)| replace:: :math:`+ \Delta H`

Reading horizontally, the rows describe the flows of funds between
sectors. Every inflow (positive value; a *source*) must have a corresponding
outflow (negative value; a *use*).

Vertically, the columns describe the evolution of each sector's financial
balance. The final row in each column describes the change in each sector's
wealth as a result of excesses/shortfalls of funds. Note that the change in the
stock of money is a negative value for households because, in the case of excess
income (savings), the funds go toward wealth accumulation.

The third row, output, is the national accounting identity that defines total
production, *Y*, as equivalent to either final demand, or factor income:

.. math::
   Y = C + G = WB

Godley and Lavoie (2007) then go on to develop a 'behavioural' version of the
above:

.. csv-table:: Behavioural (transactions) matrix for Model *SIM*
   :header: "", Households, Production, Government
   :stub-columns: 1
   :widths: 30, 15, 15, 15

   Consumption, |-Cd|, |+Cs|, ""
   Government expenditures, "", |+Gs|, |-Gd|
   [Output], "", |[Y]|, ""
   Factor income (wages), |+W.Ns|, |-W.Nd|, ""
   Taxes, |-Ts|, "", |+Td|
   Change in the stock of money, |-D(Hh)|, "", |+D(Hs)|

.. |-Cd| replace:: :math:`-C_d`
.. |+Cs| replace:: :math:`+C_s`
.. |-Gd| replace:: :math:`-G_d`
.. |+Gs| replace:: :math:`+G_s`
.. |+W.Ns| replace:: :math:`+W.N_s`
.. |-W.Nd| replace:: :math:`-W.N_d`
.. |-Ts| replace:: :math:`-T_s`
.. |+Td| replace:: :math:`+T_d`
.. |-D(Hh)| replace:: :math:`- \Delta H_h`
.. |+D(Hs)| replace:: :math:`+ \Delta H_s`

The *d* and *s* suffixes denote *demand* and *supply* and the *h* suffix
indicates household holdings of cash.

The table above expresses the wage bill as the product of the wage rate (*W*)
and employment (*N*).


.. _example-equations:

Model equations
===============


.. _example-equations-ds:

Equalising demand and supply
----------------------------

The first four equations of the model equalise demands and supplies:

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

The implication of the above equations is that the economy in this model is
demand-led and there are no supply constraints. Godley and Lavoie (2007) note
that, barring the third equation, these are strong assumptions.

Godley and Lavoie (2007) assert that, in this model, supplies and demands are
equalised by the Keynesian/Kaleckian quantity adjustment mechanism. By this
mechanism (and, in contrast to the other three candidate adjustment processes
considered), it is production that is flexible, such that producers provide as
much supply as is demanded. This is in contrast to other possible adjustment
processes, that involve either changes in prices or the use of inventories as a
buffer. Such a mechanism is arguably more applicable to a pure service economy,
rather than one that produces manufactured goods.

In summary, the above equations reflect the following behavioural assumptions:

* Firms sell whatever is demanded
* Sales are equal to output, by virtue of there being no inventories


.. _example-equations-income:

Disposable income
-----------------

Disposable income (*YD*) is defined as the wage bill earned by households, less
taxes:

.. math::
   :label: income

   YD = W . N_s - T_s

Where taxes are levied as a fixed proportion of money income, at rate |theta|:

.. math::
   :label: taxation

   T_d = \theta . W. N_s \qquad \theta < 1

.. |theta| replace:: :math:`\theta`


.. _example-equations-consumption:

Consumption function
--------------------

In this model, Godley and Lavoie (2007) specify household consumption as a
function of their current disposable income (*YD*, as described in the previous
section) and their accumulated wealth from the past (|H[-1]|):

.. math::
   :label: consumption

   C_d = \alpha _1 . YD + \alpha _2 . H_{h-1} \qquad 0 < \alpha _1 < \alpha _2 < 1

.. |H[-1]| replace:: :math:`H_{-1}`


.. _example-balances:

Financial balances
------------------

The previous equations explain the drivers of within-period transactions in the
model. This section concerns the changes in each sector's financial stocks as a
result of excesses/shortfalls in funds each period i.e. the evolution of
holdings of money, *H*.

In each period, the change in the stock of government-issued money, |H_s|, is
given by the difference between government receipts and outlays. The exogenous
variables are government outlays and the tax rate. Given these two policy
decisions, the deficit is endogenous (as a result of tax receipts being
determined by output in the economy), as is, by extension, the money stock. Any
shortfall in government revenue as a result of government expenditure is covered
by the issuance of new debt. In this simple model, this debt is simply cash
payment, which carries no interest payment:

.. math::
   :label: government-debt

   \Delta H_s = H_s - H_{s-1} = G_d - T_d

.. |H_s| replace:: :math:`H_s`

In the case of households, differences between disposable income and consumption
drive changes in stock of household wealth. Additions to cash holdings represent
the vehicle by which households save:

.. math::
   :label: household-wealth

   \Delta H_h = H_h - H_{h-1} = YD - C_d


.. _example-output-employment:

Output and employment
---------------------

The final equations of the model describe output and employment.

In this closed economy, the national income identify is as follows:

.. math::
   :label: output

   Y = C_s + G_s

where, by the income approach:

.. math::

   Y = W . N_d

This may be alternatively expressed as the following labour-demand equation:

.. math::
   :label: labour

   N_d = \frac{Y}{W}
