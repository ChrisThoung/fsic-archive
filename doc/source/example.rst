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

   Money stock, |+H|, 0, |-H|

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
