# -*- coding: utf-8 -*-
"""
markdown
========
FSIC module to parse model specifications from Markdown-formatted inputs.

"""

from collections import OrderedDict
import os
import re
import yaml

from pandas import DataFrame

from FSIC.classes.equation import Equation
from FSIC.classes.schematic import Schematic
from FSIC.utilities import merge_frames, make_comparison_function


FRONTMATTER = re.compile(
    r'''# Opening fence
        ^(?P<_fence>---)\n

        # Everything else is YAML
        (?P<_raw>(?:^.*?\n??)*?)

        # Closing fence: matches opening fence
        ^(?P=_fence)$''',
    re.MULTILINE | re.VERBOSE)

BLOCK = re.compile(
    r'''# Opening fence: three or more ` or three or more ~
        ^(?P<_fence>[`]{3,}|[~]{3,})

        # Attributes block: follows on the same line, enclosed in braces
        \s*\{(?P<_attributes>.*)\}\n

        # Everything else is code
        (?P<_raw>(?:^.*?\n??)*?)\n?

        # Closing fence: matches opening fence
        ^(?P=_fence)$''',
    re.MULTILINE | re.VERBOSE)

ATTRIBUTES = re.compile(
    r'''# Identifiers begin with '#'
        (?:[#](?P<identifier>[_A-Za-z0-9]+))|

        # Classes begin with '.'
        (?:(?P<class>[.][_A-Za-z0-9]+))|

        # Attributes are key:value pairs split by '='
        (?:(?P<attribute>
              (?P<key>[_A-Za-z0-9]+)
              \s*=\s*
              (?P<quote>['"])?(?P<value>[_A-Za-z0-9]+)(?P=quote)?))''',
    re.VERBOSE)

COMMENT = re.compile(
    r'''# Line may begin with code...
        ^(?P<code>.*?)

        # ...and end with an optional comment
        (?: # Comment character ('#') possibly with leading and trailing
            # whitespace
            \s*[#]\s*

            # Comment content
            (?P<comment>.*?))?

        # Ignore trailing whitespace to the end of the line
        \s*$
    ''',
    re.MULTILINE | re.VERBOSE)


def read_markdown(filepath_or_string):
    """Read the model specification in `filepath_or_string`.

    Parameters
    ----------
    filepath_or_buffer : str
        Markdown input to read. Can be either a path to the input file or a
        string of formatted Markdown.

    Returns
    -------
    schematic : `FSIC` `Schematic` object
        The parsed model specification

    """
    if os.path.exists(filepath_or_string):
        filepath_or_string = open(filepath_or_string, 'r').read()

    blocks = parse_blocks(filepath_or_string)

    schematic = Schematic()
    schematic.block_table = DataFrame.from_dict(
        blocks, orient='index').reindex(index=blocks.keys())

    schematic.equations, block_mapping = make_equations_dicts(
        schematic.block_table)
    schematic.equation_table = DataFrame.from_dict(
        block_mapping, orient='index').reindex(block_mapping.keys())

    schematic.symbol_table = make_symbol_table(schematic.equations)
    return schematic


def parse_blocks(string):
    """Return the parsed blocks of the Markdown `string` as an `OrderedDict` of `dicts`.

    Returns
    -------
    blocks : `OrderedDict`
        Parsed code blocks, with:
         - key: the block identifier (or a numbered default name with prefix
                'Unnamed_Block_')
         - value: a dictionary of block data (see notes for naming conventions)

        The variable *always* contains an entry with key '_Frontmatter' with
        class '.yaml'.

    Notes
    -----
    The contents of the inner dictionaries (corresponding to the individual
    blocks) are as follows:
     - key: '_raw'
       value (str): the code between the fences of the code block
       notes: always present

     - key: '.*' (str beginning with '.')
       value (bool): `True` if the class was included in this code block's
                     attributes section; `False` otherwise

     - key: [any other string]
       value (str): the value to accompany the attribute's key;
                    '' (empty string) otherwise

    """
    blocks = OrderedDict()
    # Process frontmatter
    frontmatter = {}
    fm = FRONTMATTER.match(string)
    if fm:
        frontmatter = fm.groupdict()
        del frontmatter['_fence']
        string = string[fm.end():]
    frontmatter['.yaml'] = True
    blocks['_Frontmatter'] = frontmatter.copy()
    # Parse blocks
    counter = 0
    for match in BLOCK.finditer(string):
        name, contents = _parse_block(match.groupdict())
        if name is None:
            name = 'Unnamed_Block_{}'.format(counter)
            counter += 1
        blocks[name] = contents
    # Form complete list of classes and attributes
    classes = [k
               for b in blocks.values()
               for k in b.keys()
               if k.startswith('.')]
    attributes = [k
                  for b in blocks.values()
                  for k in b.keys()
                  if k[0] != '.']
    # Fill in classes and attributes for all blocks
    for k in blocks.keys():
        for c in classes:
            if c not in blocks[k]:
                blocks[k][c] = False
        for a in attributes:
            if a not in blocks[k]:
                blocks[k][a] = ''
    return blocks

def _parse_block(dict_):
    """Return the name and processed contents of `dict_`."""
    # Initialise final return variables
    name = None
    contents = dict_.copy()
    del contents['_fence']
    # Process attributes list
    attributes = contents.pop('_attributes')
    for match in ATTRIBUTES.finditer(attributes):
        item = {k: v for k, v in match.groupdict().items() if v}
        assert len(item) == 1 or 4
        if len(item) == 1:
            key, value = list(*item.items())
            if key == 'identifier':
                name = value
            elif key == 'class':
                contents[value] = True
        elif len(item) == 4:
            key, value = item['key'], item['value']
            contents[key] = value
    return name, contents


def make_equations_dicts(block_table):
    equations = OrderedDict()
    block_mapping = OrderedDict()
    for name, row in block_table.iterrows():
        if row.get('.python', False) and not row.get('.hidden', False):
            for match in COMMENT.finditer(row['_raw']):
                code = match.group('code').strip()
                if not len(code):
                    continue
                equation = Equation(code)
                key = equation.template.format(
                    **equation.terms['normalised'].to_dict())
                equations[key] = equation
                block_mapping[key] = {'block': name}
    return equations, block_mapping


def make_symbol_table(equations):
    """Return the combined symbol tables in `equations`."""

    def compare_equation_strings(a, b):
        if len(a) and len(b):
            raise SpecificationError
        elif not len(a) and not len(b):
            return ''
        elif len(a) > len(b):
            return a
        else:
            return b

    symbol_tables = []
    for key, equation in equations.items():
        symbols = equation.symbols.copy()
        symbols['equation'] = ''
        for index, row in symbols.iterrows():
            if row['type'] == 'endogenous':
                symbols.ix[index, 'equation'] = key
        symbol_tables.append(symbols)

    return merge_frames(
        symbol_tables,
        {'type': make_comparison_function(Equation.PRECEDENCE,
                                          Equation.EXCLUSIVE),
         'min': min,
         'max': max,
         'equation': compare_equation_strings})
