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

.. csv-table:: The balance sheet of Model SIM
   :header: "", "1. Households", "2. Production", "3. Government"
   :stub-columns: 1
   :widths: 25, 15, 15, 15

   "Money stock", "+H", 0, "-H"

As an asset to households, money appears as a positive entry on their balance
sheet. For the government, as the holder of the corresponding liability, the
relevant entry on the balance sheet is negative.
