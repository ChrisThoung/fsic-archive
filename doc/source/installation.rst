.. _installation:

************
Installation
************


.. _installation-obtain:

Obtaining FSIC
==============

The latest version of FSIC is available from GitHub_.

.. _GitHub: https://github.com/cthoung/fsic


.. _installation-install:

Installing FSIC
===============

After downloading the source code, FSIC can be installed from the command line,
like any other standard Python package distribution, as follows::

    python setup.py install


.. _installation-test:

Running the test suite
======================

FSIC includes a test suite that uses nose_. These tests can be run as follows,
while in the root folder of the source code::

    nosetests

Running the tests with the following further options also displays the tests'
coverage of the code::

    nosetests --with-coverage --cover-package=FSIC

.. _nose: https://nose.readthedocs.org/en/latest/


.. _installation-doc:

Building the documentation
==========================

The documentation for FSIC (this documentation) is written using Sphinx_. The
``doc`` folder contains all the files necessary to build the documentation in a
variety of output formats. For example, to build the html version of the
documentation from the command line, run::

    make html

See the ``makefile`` for further information on the available output formats.

.. _Sphinx: http://sphinx-doc.org/
