"""Check if a collection of vectors is an Unextendable Product Basis (UBP)."""

from itertools import combinations
import numpy as np

def item_partitions(items, parts, sizes = None ):
    if sizes == None:
        sizes = [1]*parts

    if parts == 1:
        return [items]
    
    partitions = []
    min_choices = sizes[0]
    max_choices = len(items) - sum(sizes[i] for i in range(1,parts))
    for j in range(min_choices, max_choices + 1):
        first_part = combinations(items, j)
        for part1 in first_part: 
            unchosen_items = [item for item in items if item not in list(part1)]
            other_parts = item_partitions(unchosen_items, parts - 1, sizes[1:])
            for part2 in other_parts:
                partition = [list(part1)] + [part2]
                partitions.append(partition)
    return partitions