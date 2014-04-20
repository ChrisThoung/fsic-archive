# -*- coding: utf-8 -*-
"""
chunk
=====
FSIC parser to convert code chunks into Dictionary objects.

"""


import re


def split(chunk):
    """Split `chunk` into an attributes string and a code string.

    Parameters
    ==========
    chunk : string
        Code chunk to split

    Returns
    =======
    contents : Dictionary
        Contains:
            'attributes' : string
                Code-block attributes
            'code' : string
                The code itself

    """
    pattern = re.compile(
        r'''^[~`]{3,}                   # Chunk begins with at least three
                                        # tildes or backticks at the start
                                        # of a line
            \{(?P<attributes>.+?)\}\n   # Attributes inside braces
            (?P<code>.*?)               # Remainder is code
            ^[~`]{3,}$                  # Chunk ends with at least three
                                        # tildes or backticks at the start
                                        # of a line
        ''',
        re.DOTALL | re.MULTILINE | re.VERBOSE)
    m = pattern.search(chunk)
    contents = {
        'attributes': m.group('attributes').strip(),
        'code': m.group('code').strip()
        }
    return contents


def parse_attributes_block_identifier(block):
    """Return the identifier in `block`.

    Parameters
    ==========
    block : string
        Block to search in

    Returns
    =======
    Either:
        identifier : string
            If identifier found
        None
            If no identifier found

    """
    pattern = re.compile(r'#(?P<identifier>\w+\b)')
    instances = len(pattern.findall(block))
    if instances > 1:
        raise ValueError(
            'Found ' +
            str(instances) +
            ' identifiers; expected at most one')
    s = pattern.search(block)
    if s == None:
        return None
    else:
        return s.group('identifier')


def parse_attributes_block_classes(block):
    """Return the classes in `block`.

    Parameters
    ==========
    block : string
        Block to search in

    Returns
    =======
    classes : list of strings (empty if none found)

    """
    pattern = re.compile(r'[.]\w+\b')
    s = pattern.findall(block)
    s = [c[1:] for c in s]
    return s


def parse_attributes_block_attributes(block):
    """Return the attributes in `block`.

    Parameters
    ==========
    block : string
        Block to search in

    Returns
    =======
    attributes : Dictionary

    Notes
    =====
    Attributes are key:value pairs of the form:
        x="y"
    which convert to Dictionary entries:
        'x': 'y'

    Values are left as strings

    """
    pattern = re.compile(r'\w+\s*=\s*".+?"')
    s = pattern.findall(block)
    attributes = {}
    for i in s:
        parts = i.partition('=')
        parts = [p.strip() for p in parts]
        k, v = parts[0::2]
        if k in attributes:
            raise ValueError('Duplicate keys found in attributes block')
        attributes[k] = v[1:-1]
    return attributes


def parse_attributes_block(block):
    """Convert `block` into a Dictionary of attributes.

    Parameters
    ==========
    block : string
        Extract from the attributes block of a code chunk

    Returns
    =======
    attributes : Dictionary
        Contains:
            'identifier' : string
                The name of the code block (`None` if not supplied);
                preceded by '#'; one instance per block only
            'classes' : list
                Any attributes (empty if none supplied);
                words preceded by '.'; multiple instances per block
                permitted; duplicates permitted
            attributes : strings
                Keyword-type attributes are split into their key:value
                pairs; 'identifier' and 'classes' are reserved keywords;
                duplicates not permitted

    Notes
    =====
    Example 1:
        block = '#consumption .python .postkeynesian type="not hydraulic"'
        `attributes` would contain:
            'identifier' : consumption
            'classes' : ['python', 'postkeynesian']
            'type' : 'not hydraulic'

    Example 2:
        block = ''
        `attributes` would contain:
            'identifier' : None
            'classes' : []

    """
    # Extract identifier and classes
    identifier = parse_attributes_block_identifier(block)
    classes = parse_attributes_block_classes(block)
    # Extract attributes and use as starting variable to return
    attributes = parse_attributes_block_attributes(block)
    attributes['identifier'] = identifier
    attributes['classes'] = classes
    # Return
    return attributes
