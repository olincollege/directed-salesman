"""
Implementation and testing of the Held-Karp algorithm
https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm
"""
from typing import *
import networkx as nx
from utils import random_graph
import random
from bitset import BitSet


def _held_karp_pt1(graph: nx.Graph, nodes: BitSet, target: int) -> Tuple[float, List[int]]:
    """
    Runs the first step of the Held-Karp algorithm.

    Finds the shortest path from 0 to `n` going through all of `nodes`.

    :param graph: the Graph to find the path through, with nodes labeled 0, 1, ...
    :param nodes: a bitstring representation of the set of nodes to pass through
    :param n: the node to end at
    :return: a tuple, first the length of the path, and then the order of the nodes
    """
    print(f'{nodes = } (empty? {nodes.isempty()}), {nodes.value = } {target = }')
    if target in nodes:
        raise ValueError(f'The target vertex {target} should not be in nodes ({bin(nodes)})')
    if 0 in nodes:
        raise ValueError(f'The starting vertex (0) should not be in nodes ({bin(nodes)})')
    if nodes.isempty():
        return graph[0][target]['weight'], [0, target]

    shortest_dist = -1
    shortest_path = []

    # Let i be the node before the target
    for i in range(1, len(graph)):
        if i not in nodes:  # If it's the node before the target, then it must be in nodes
            continue
        s_i = nodes.difference(BitSet(len(graph), {i}))
        print(f'Removed {i} from {nodes} to get {s_i}')
        dist, path = _held_karp_pt1(graph, s_i, i)  # find shortest path to i through s_i
        act_dist = dist + graph[i][target]['weight']  # actual len is len above plus len i -> target
        if shortest_dist == -1 or act_dist < shortest_dist:
            shortest_dist = act_dist
            shortest_path = path
    assert shortest_dist > 0
    shortest_path.append(target)  # path did not include target - add it
    return shortest_dist, shortest_path


def held_karp(graph: nx.Graph) -> Tuple[float, List[int]]:
    """
    Runs the Held-Karp algorithm to solve TSP

    :param graph: the Graph to find a path through, with nodes labeled 0, 1, ...
    :return: a tuple, the length of the shortest complete cycle, the order of the nodes
    """
    num_nodes = len(graph)
    shortest_dist = -1
    shortest_path = []
    all_nodes = BitSet(len(graph) - 1, {0}).complement()
    print(bin(all_nodes.value))
    for target in range(1, num_nodes):
        nodes = all_nodes.difference(BitSet(len(graph), {target}))
        dist, path = _held_karp_pt1(graph, nodes, target)
        act_dist = dist + graph[target][0]['weight']
        if shortest_dist == -1 or act_dist < shortest_dist:
            shortest_dist = act_dist
            shortest_path = path
    return shortest_dist, shortest_path
