"""
Implementation and testing of the Held-Karp algorithm
https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm
"""
import itertools
from typing import *
import networkx as nx
from bitset import BitSet


def held_karp(graph: nx.Graph) -> Tuple[float, List[int]]:
    """
    Runs the Held-Karp algorithm to solve TSP

    :param graph: the Graph to find a path through, with nodes labeled 0, 1, ...
    :return: a tuple, the length of the shortest complete cycle, the order of the nodes
    """
    # Setup
    cache = {}
    num_nodes = len(graph)
    make_bitset = lambda s: BitSet(num_nodes, s)
    for k in range(1, num_nodes):
        cache[(make_bitset(1 << k), k)] = graph[0][k]['weight'], [0, k]

    # Part 1: populate cache
    for subset_size in range(2, num_nodes):
        for subset_lst in itertools.combinations(range(1, num_nodes), r=subset_size):
            subset = make_bitset(set(subset_lst))
            for k in subset_lst:
                shortest = -1, []
                for m in subset_lst:
                    if m == k:
                        continue
                    dist, path = cache[(subset.difference(make_bitset(1 << k)), m)]
                    act_dist = dist + graph[m][k]['weight']
                    if shortest[0] == -1 or act_dist < shortest[0]:
                        shortest = act_dist, path + [k]
                cache[(subset, k)] = shortest

    # Part 2: Find the shortest path from cache
    shortest = -1, []
    all_nodes = make_bitset(2 ** num_nodes - 2)
    for k in range(1, num_nodes):
        dist, path = cache[(all_nodes, k)]
        act_dist = dist + graph[k][0]['weight']
        if shortest[0] == -1 or act_dist < shortest[0]:
            shortest = act_dist, path

    return shortest[0], shortest[1] + [0]
