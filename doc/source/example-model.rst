.. _example-model:

************************************
Godley and Lavoie's (2007) Model SIM
************************************

This section is the first of two, to illustrate how to build and run a model
using FSIC. It uses Godley and Lavoie's (2007) *Model SIM* as an example.

This first section sets out the structure and equations of the model. The next
section goes on to describe how to specify and build the model, in order to
conduct simulations.


.. _example-model-intro:

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


.. _example-model-accounts:

Accounting matrices
===================

*Model SIM* is underpinned by a complete set of accounts that describe the
transactions in each period (*flows* of funds between sectors) and the
implications for sectors' balance sheets (their financial *stocks*).

The balance sheet for *Model SIM* consists of just one item: money, which is
printed by the government and assumed to consist entirely of banknotes. This is
*cash* or *high-powered* money. Money (*H*) is an asset of households and a
corresponding liability for the government, hence the positive and negative
signs in the table below:

.. csv-table:: The balance sheet of Model *SIM*
   :header: "", Households, Production, Government
   :stub-columns: 1
   :widths: 30, 15, 15, 15

   Money stock, |+H_h|, "", |-H_s|

.. |+H_h| replace:: :math:`+H_h`
.. |-H_s| replace:: :math:`-H_s`

This balance sheet evolves through time through the accumulation and depletion
of money holdings. These changes arise from excesses and shortfalls of funds
each period, in the course of sectors' transactions.

Godley and Lavoie's (2007) 'behavioural' version of the transactions matrix is
as follows, where the columns represent institutional sectors of the model and
the rows represent transactions between those sectors:

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
.. |[Y]| replace:: :math:`[Y]`
.. |+W.Ns| replace:: :math:`+W.N_s`
.. |-W.Nd| replace:: :math:`-W.N_d`
.. |-Ts| replace:: :math:`-T_s`
.. |+Td| replace:: :math:`+T_d`
.. |-D(Hh)| replace:: :math:`- \Delta H_h`
.. |+D(Hs)| replace:: :math:`+ \Delta H_s`

The *d* and *s* suffixes denote *demand* and *supply* and the *h* suffix
indicates household holdings of cash. Factor income (the wage bill) is the
product of the wage rate (*W*) and employment (*N*). The third row, output, is
the national accounting identity that defines total production, *Y*, as
equivalent to either final demand, or factor income:

.. math::
   Y = C + G = WB

Reading along the rows, every outflow of funds (a negative value; a *use*) must
show up as an inflow to another (a positive value; a *source*), such that the
sum of each row comes to zero.

Each column describes a sector's uses and sources of funds. Where the sum of
uses and the sum of sources in the first five rows are not equal, there must be
an excess or shortfall of funds. This translates into a change in the stock of
money in the sixth and final column. It is this final row that describes the
evolution of the balance sheet.

Note that the change in the stock of money is a negative value for households
because, in the case of excess income (savings), the funds go toward wealth
accumulation.


.. _example-model-equations:

Model equations
===============


.. _example-model-equations-ds:

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


.. _example-model-equations-income:

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


.. _example-model-equations-consumption:

Consumption function
--------------------

In this model, Godley and Lavoie (2007) specify household consumption as a
function of their current disposable income (*YD*, as described in the previous
section) and their accumulated wealth from the past (|H[-1]|):

.. math::
   :label: consumption

   C_d = \alpha _1 . YD + \alpha _2 . H_{h-1} \qquad 0 < \alpha _1 < \alpha _2 < 1

.. |H[-1]| replace:: :math:`H_{-1}`


.. _example-model-balances:

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


.. _example-model-output-employment:

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


.. _example-model-redundant:

The redundant equation
----------------------

As set out above, household accumulation and government issuance of money are
entirely separate processes. There is no explicit equilibrium condition that
ensures equality between the two.

However, by the design of the model's accounts, holdings and issuances of money
*must* in fact be equal. The accounting principles that underpin the model, and
the assumptions that equalise demand and supply.

Godley and Lavoie (2007) refer to this result as a 'quasi-Walrasian' principle,
by which any properly-constructed model must contain an equation that is
'redundant', by virtue of it being logically implied by the others. Indeed, such
an equation's exclusion is necessary, so as to ensure that the model's solution
is not over-determined.

In the current model, this redundant equation is:

.. math::
   \Delta H_h = \Delta H_s

That is, the above equation reflects the Keynesian identity that states that
investment must be equal to saving. In a model such as this, with no investment,
there can be no social saving by the economy as a whole. As such, household
saving is matched exactly by government dissaving.

In contrast to conventional models, in which market clearing (or otherwise) is a
*determinant* of macroeconomic phenomena, Godley and Lavoie (2007) stress that
these equalities between demand and supply are a *consequence* of a model with a
comprehensive system of accounts. A neo-classical model would instead
incorporate an equilibrium condition that brings the demand for money in line
with an exogenously-determined money supply.


.. _example-model-summary:

Summary
=======

As set out above, the model has 11 equations and 11 unknowns. Of the variables
in the model, three are exogenous: |G_d|, |theta| and |W|. The first two,
government expenditure and the tax rate, are fiscal policy variables while the
third is assumed to be fully exogenous for the purposes of the example.

As Godley and Lavoie (2007) note, a crucial feature of the model is its
dependence on stock variables that affect the evolution of the economy through
time.

.. |G_d| replace:: :math:`G_d`
.. |W| replace:: :math:`W`
