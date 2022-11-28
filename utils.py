"""
Utility functions
"""
import itertools
import networkx as nx
import random


def random_graph(n: int) -> nx.Graph:
    """
    Generates a random graph on n nodes (0 - n-1)

    :param n: an int, the number of nodes in the graph
    :return: a randomly generated Graph with n nodes
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    points = [(random.random(), random.random()) for _ in range(n)]
    # for each pair of nodes, calculate distance and add weighted edge
    graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                          + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                  for i, j in itertools.combinations(range(n), 2))

    return graph
