.. _installation:

************
Installation
************


.. _installation-obtain:

Obtaining FSIC
==============

The latest version of FSIC is available from GitHub_.

.. _GitHub: https://github.com/cthoung/fsic


.. _installation-requirements:

Requirements
============

FSIC has been developed and tested on Python 3.2-3.4. See the main
``README.md`` file for the most up-to-date list of other dependencies.

.. Note::
   Throughout this documentation, the Python interpreter is assumed to be
   listed in the system ``PATH`` variable with name ``python`` e.g. ``python
   setup.py install``. This may differ between systems. For example in recent
   versions of `Ubuntu Linux`_, Python may be installed with name ``python3``,
   ``python3.4`` etc. Where applicable, the user should substitute with the
   appropriate call.

.. _`Ubuntu Linux`: http://www.ubuntu.com/


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

.. Note::
   As with the ``python`` interpreter, the ``nosetests`` program may have a
   different name e.g. ``nosetests3``.


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
