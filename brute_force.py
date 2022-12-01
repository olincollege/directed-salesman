"""
Implementation and testing of a Brute Force Search algorithm
"""
import itertools
from typing import *
import networkx as nx
from utils import *


def brute_force(graph: nx.Graph) -> Tuple[float, List[int]]:
    """
    Finds the shortest path within the given graph with a brute-force approach

    :param graph: the nx.Graph to find the shortest path on
    :return: a tuple - first a float giving the length of the path, and then a list of ints giving the path
    """
    best_length = -1
    best_path = None
    for path in itertools.permutations(range(1, len(graph))):
        actual_path = [0]
        actual_path.extend(path)
        actual_path.append(0)
        length = length_of_path(graph, actual_path)
        if best_length == -1 or length < best_length:
            best_length = length
            best_path = actual_path
    return best_length, best_path
