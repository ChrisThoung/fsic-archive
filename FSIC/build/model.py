# -*- coding: utf-8 -*-
"""
model
=====
Build FSIC models from `Schematic` objects.

"""

from collections import OrderedDict
import itertools
import yaml

from FSIC.analysis.graph import make_graph, topological_sort
from FSIC.classes.model import Model
from FSIC.templates.python import MODEL, DEFAULT_FIELDS, MAIN_BLOCK


def order_method_topological(equations):
    return itertools.chain.from_iterable(
        topological_sort(make_graph(equations)))


ORDER_METHODS = OrderedDict(zip(*zip(
    ['topological', order_method_topological],
    ['none', lambda x: x])))


def build_model(schematic, output='class', with_main=False, order_method='topological', **kwargs):
    """Create a FSIC model class from `schematic`.

    ** Warning: if `output`='class', this function uses `exec()` and `eval()`
                to return the class definition. **

    Parameters
    ----------
    schematic : `FSIC` `Schematic` object
        Input model specification
    output : string, one of ['class', 'script'] or a filename; default 'class'
        Set the output (see 'Returns' below for details)
    with_main : bool
        If `True`, add a command-line interface as an
        `if __name__ == '__main__'`-type block. No effect if `output`='class'
    order_method : string, default 'topological'
        The method to use to reorder the system of equations before assembling
        the final output. If `None`, preserve the order as it appears in the
        original input
    **kwargs : other keyword arguments to insert into class definition

    Returns
    -------
    Depends on `output`:
     - 'class' : class
           The model class as a Python object, to be instantiated. Never
           includes a 'main' block
     - 'script' : string
           An `exec`utable string (the same one used to return a class
           definition if `output`='class'). May include a 'main' block
     - filename : None
           Instead of returning anything, write the script to the path in
           `filename`. May include a 'main' block

    """
    # Use default dictionary as a starting point, and copy in frontmatter
    contents = DEFAULT_FIELDS.copy()
    frontmatter = yaml.load(schematic.block_table.ix['_Frontmatter', '_raw'])
    if frontmatter is not None:
        for k, v in frontmatter.items():
            contents[k] = v

    # Insert variable information
    variable_types = {'endogenous': 'endogenous',
                      'exogenous': 'exogenous',
                      'parameters': 'parameter',
                      'errors': 'error'}
    for key, type_ in variable_types.items():
        contents[key] = [v for v, t in schematic.symbol_table['type'].items()
                         if t == type_]
    contents['variables'] = contents['endogenous'] + contents['exogenous']
    contents['convergence_variables'] = contents['endogenous']

    # Add offset values
    contents['start_offset'] = -min(schematic.symbol_table['min'])
    contents['end_offset'] = max(schematic.symbol_table['max'])

    # Overwrite with any additional keyword arguments
    for k, v in kwargs.items():
        contents[k] = v

    # Order the system of equations using the selected method
    try:
        order_method = str(order_method).lower()
        order_function = ORDER_METHODS[order_method]
        order = order_function(schematic.equations)
    except KeyError:
        raise ValueError(
            'Unrecognised value passed to `order_method`: {}'.format(
                order_method))

    # Create final code for Python solution
    lines = []
    for item in order:
        equation = schematic.equations[item]
        format_dict = {}
        for i, t in equation.terms.iterrows():
            key = t.name
            term = t['name']
            if t['type'] in ('endogenous', 'exogenous', 'parameter', 'error'):
                index = t['index']
                if index == 0:
                    index = ''
                term = 'self.{variable}.values[row{index}]'.format(
                    variable=t['name'], index=index)
            format_dict[key] = term
        expression = equation.template.format(**format_dict)
        lines.append(expression)
    contents['python_code'] = '\n        '.join(lines)

    # Create underline to match length of model name
    contents['underline'] = '=' * len(contents['name'])

    # Remove trailing whitespace and ensure version information is a string, if
    # necessary
    for k in contents.keys():
        try:
            contents[k] = contents[k].rstrip()
        except AttributeError:
            pass
    contents['version'] = repr(contents['version'])

    template = MODEL
    if output != 'class' and with_main:
        template += MAIN_BLOCK
    script = template.format(**contents)

    if output == 'class':
        exec(script)
        return eval(contents['name'])
    elif output == 'script':
        return script
    else:
        with open(output, 'w') as f:
            print(script, file=f)
