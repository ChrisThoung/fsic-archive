.. _io:

I/O
===

FSIC includes I/O functions to read and write CSV data, possibly with `YAML
frontmatter`_. This is mainly to ease data input for model solution, but the
functions are available for direct use.

.. _YAML frontmatter: http://blog.datacite.org/using-yaml-frontmatter-with-csv/


:func:`FSIC.read_csvy()` is a wrapper that passes arguments to
``pandas.read_csv()``. For 'regular' CSV files, the result is the same as a
call to ``pandas.read_csv()``. However, if the input file has YAML frontmatter,
:func:`FSIC.read_csvy()` can distinguish this frontmatter from the CSV data.

.. function:: FSIC.read_csvy(filepath_or_buffer, *args, return_frontmatter=False, **kwargs)

   Wrapper for ``pandas.read_csv()``, to allow for YAML frontmatter.

   :param filepath_or_buffer: input to read, as for ``pandas.read_csv()``

   :param return_frontmatter: return YAML frontmatter alongside the data, as a 2-tuple
   :type return_frontmatter: boolean

   :param args: additional arguments, as for ``pandas.read_csv()``
   :param kwargs: additional arguments, as for ``pandas.read_csv()``

   :returns: CSV data ``df`` (, frontmatter ``fm``, if ``return_frontmatter`` is ``True``)
   :rtype: ``DataFrame`` (, ``dict`` if ``return_frontmatter`` is ``True``)

   :See also: ``pandas.read_csv()``
