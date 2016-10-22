# -*- coding: utf-8 -*-
"""
schematic
=========
`Schematic` class to store complete model specifications.

"""

from collections import Counter


class Schematic(object):
    """FSIC class to store a complete model specification."""

    def __init__(self):
        self.block_table = None
        self.equations = None
        self.equation_table = None
        self.symbol_table = None

    @staticmethod
    def merge(schematics):
        """Merge the objects in `schematics` into a single `Schematic`.

        Parameters
        ----------
        schematics : iterable of `Schematic` objects
            Objects to merge

        Returns
        -------
        schematic : FSIC `Schematic` object
            The combined schematic

        """
        # TODO: Consider an alternative way to work around the circular
        #       dependency between the `Schematic` class and
        #       `process_block_table()`
        from fsic.parser.markdown import process_block_table

        block_table = None
        for s in schematics:
            if block_table is None:
                block_table = s.block_table
            else:
                # TODO: Implement cleaner suffixing for when number of
                #       schematics >2
                block_table = _merge_block_tables(block_table, s.block_table)

        schematic = Schematic()
        (schematic.block_table,
         schematic.equation_table,
         schematic.symbol_table,
         schematic.equations) = process_block_table(block_table)

        return schematic


def _merge_block_tables(old, new):
    """Merge two block tables into a single table.

    Parameters
    ----------
    old, new : `pandas` `DataFrame`s
        Block tables to merge

    Returns
    -------
    merged : `pandas` `DataFrame`
        Combined block table

    """
    # Resolve cases where both tables contain a frontmatter block
    if '_Frontmatter' in old.index and '_Frontmatter' in new.index:
        # New block table has empty frontmatter entry: just drop
        if len(new.loc['_Frontmatter', '_raw'].strip()) == 0:
            new = new.drop('_Frontmatter', axis='index')
        else:
            raise NotImplementedError(
                'Unimplemented case for block tables '
                'that both contain a frontmatter block')

    merged = old.append(new).fillna(False)

    # If duplicate names across tables, rename with a '_n' suffix,
    # where n is a zero-based counter
    if merged.index.has_duplicates:
        num_instances = Counter(merged.index)
        count = Counter()
        index = list(merged.index)
        for i, row in enumerate(merged.index):
            if num_instances[row] > 1:
                index[i] = '{}_{}'.format(row, count[row])
                count[row] += 1
        merged.index = index

    return merged
