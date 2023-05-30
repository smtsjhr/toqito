"""Check if a collection of vectors is an Unextendable Product Basis (UBP)."""

from itertools import combinations
import numpy as np
from scipy.linalg import null_space


def item_partitions(items, parts, sizes = None ):
    if sizes == None:
        sizes = [1]*parts

    if parts == 1:
        return [[items]]
    
    partitions = []
    min_choices = sizes[0]
    max_choices = len(items) - sum(sizes[i] for i in range(1,parts))
    for j in range(min_choices, max_choices + 1):
        first_part = combinations(items, j)
        for part1 in first_part: 
            unchosen_items = list(set(items) - set(part1))
            other_parts = item_partitions(unchosen_items, parts - 1, sizes[1:])
            for part2 in other_parts:
                partition = [list(part1)] + part2
                partitions.append(partition)
    return partitions


def is_unextendible_product_basis(local_vectors):

    num_parties = len(local_vectors)
    num_states = local_vectors[0].shape[1]
    local_dimensions = [party.shape[0] for party in local_vectors]
    state_index = [i for i in range(num_states)]

    partitions = item_partitions(state_index, num_parties, [dim - 1 for dim in local_dimensions])
    num_partitions = len(partitions)

    if num_partitions == 0:
        isUPB = False
        orth_states= []
        num_orth = 0
        for party in range(num_parties):
            if num_orth >= num_states:
                orth_state = np.zeros((local_dimensions[party], 1))
                orth_state[party][1] = 1
                witness.append(orth_state)
            else:
                more_orth = min([local_dimensions[party] - 1, num_states - num_orth])
                local_choices = [num_orth + i for i in range(more_orth + 1)]
                local_states = local_vectors[party][:, local_choices]
                local_orth_states = null_space(local_states.T)
                if local_orth_states.size == 0:
                    orth_states.append([])
                else:
                    orth_states.append(local_orth_states[:, 0])
                num_orth += more_orth
        witness = orth_states
        return (isUPB, witness)


    for partition in partitions:
        num_orth_states = 1
        orth_states = []
        for party, states in enumerate(local_vectors):
            local_choices = partition[party]
            local_states = states[ : , local_choices]
            local_orth_states = null_space(local_states.T)
            if local_orth_states.size == 0:
                num_local_orth_states = 0
            else:
                num_local_orth_states = local_orth_states.shape[1]
            num_orth_states *= num_local_orth_states
            if num_orth_states == 0:
                break    
            orth_states.append(local_orth_states[:, 0])    
        if num_orth_states >= 1:
            isUPB = False
            witness = orth_states
            return (isUPB, witness)

    isUPB = True
    witness = None    
    return (isUPB, witness)