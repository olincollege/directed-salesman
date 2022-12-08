"""
Implementation and testing of a Brute Force Search algorithm
"""
import itertools
from typing import *
import networkx as nx

import utils
from utils import *


def _brute_force_rec(graph: nx.Graph, path: Set[int], last_node: int) -> Tuple[float, List[int]]:
    """
    Recursively implements a brute-force algorithm to find the solution to the TSP

    All solutions provided by this function will start with the given path

    :param graph: a nx.Graph, the graph to search
    :param path: a set of ints, the nodes that have already been traversed
    :param last_node: an int, the most recent node to be visited
    :return: a tuple - first a float giving the length of the shortest remaining path, and then a list of ints giving
        the remainder of the path, reversed
    """
    if len(path) == len(graph) - 1:
        print(f'Going from {last_node} to 0 is a dist of {graph[last_node][0]["weight"]}')
        return graph[last_node][0]['weight'], []
    shortest_dist = -1
    shortest_path = []
    for node in range(1, len(graph)):
        if node in path:
            continue
        path.add(node)
        dist, rem_path = _brute_force_rec(graph, path, node)
        path.remove(node)
        act_dist = dist + graph[last_node][node]['weight']
        if shortest_dist == -1 or act_dist < shortest_dist:
            shortest_dist = act_dist
            shortest_path = rem_path
            shortest_path.append(node)
    print(f'The best remaining path after going through {path} is {shortest_path} with dist {shortest_dist}')
    return shortest_dist, shortest_path


def brute_force(graph: nx.Graph) -> Tuple[float, List[int]]:
    """
    Finds the shortest path within the given graph with a brute-force approach

    :param graph: the nx.Graph to find the shortest path on
    :return: a tuple - first a float giving the length of the path, and then a list of ints giving the path
    """
    dist, rev_path = _brute_force_rec(graph, set(), 0)
    return dist, [0] + rev_path[::-1] + [0]
