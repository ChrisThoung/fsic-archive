.. _bonnet-data:

********************
FSIC internals: Data
********************

This section provides further technical information on the internals of a
FSIC-generated model. Specifically, this section concerns the storage of data
during a model run.


.. _bonnet-data-internal:

Internal
========

During the build process that transforms the raw Markdown code into a complete
model script, FSIC identifies the component variables of the model. On
initialisation of the model, a set of pandas Series objects are created as
member variables. This allows for the individual variables to be manipulated in
the calling code, as in the following example (where the model object has name
``SIM``)::

    SIM.G_d.ix[1960:] = 20

The complete set of variable values through time can be accessed with a call to
``get_results()``::

    complete_results = SIM.get_results()

The return variable is a data frame containing the complete set of variables
(as identified in the original Markdown file).


.. _bonnet-data-output:

Output
======



.. _bonnet-data-input:

Input
=====

While the ``FSIC.io`` module provides various tools to read in data from a
range of file formats, the standard model template requires the final input
variable to update the database to be a pandas DataFrame with structure as
follows:

.. csv-table:: The balance sheet of Model *SIM*
   :header: Column, Type, Contents
   :widths: 10, 15, 15

   0, PeriodIndex, DataFrame index
   1, dtype, Variable
   2, dtype, Variable
   ., ., .
   ., dtype, Variable
   ., ., .
   n, dtype, Variable
