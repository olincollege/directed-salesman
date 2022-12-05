"""
Utility functions
"""
import itertools
import networkx as nx
import random
import math


def random_graph(n: int, is_directed: bool = False) -> nx.Graph:
    """
    Generates a random graph on n nodes (0 - n-1)

    :param n: an int, the number of nodes in the graph
    :return: a randomly generated Graph with n nodes
    """
    if is_directed:
        graph = nx.DiGraph()
        graph.add_nodes_from(range(n))
        points = [(random.random(), random.random()) for _ in range(n)]
        # for each pair of nodes, calculate distance and add weighted edge
        graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                              + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                      for i, j in itertools.combinations(range(n), 2))
        points = [(random.random(), random.random()) for _ in range(n)]
        graph.add_weighted_edges_from((j, i, ((points[i][0] - points[j][0]) ** 2
                                              + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                      for i, j in itertools.combinations(range(n), 2))

    else:
        graph = nx.Graph()
        graph.add_nodes_from(range(n))
        points = [(random.random(), random.random()) for _ in range(n)]
        # for each pair of nodes, calculate distance and add weighted edge
        graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                              + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                      for i, j in itertools.combinations(range(n), 2))
    return graph

def circle_graph(n: int, is_directed: bool = False) -> nx.Graph:
    """
    Generates a complete graph of the outline of a circle

    :param n: an int, the number of nodes in the graph
    :return: a circular Graph with n nodes
    """
    graph = nx.DiGraph()
    #graph.add_nodes_from(range(n))
    points = []
    step_size_rad = 2 * math.pi / n
    for k in range(n):
        angle = k * step_size_rad
        point = (math.sin(angle), math.cos(angle))
        points.append(point)
        graph.add_node(k, pos=point)

    # for each pair of nodes, calculate distance and add weighted edge
    graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                            + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                    for i, j in itertools.combinations(range(n), 2))
    graph.add_weighted_edges_from((j, i, ((points[i][0] - points[j][0]) ** 2
                                            + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                    for i, j in itertools.combinations(range(n), 2))
    return graph

def rectangle_graph(n: int, m: int, is_directed: bool = False) -> nx.Graph:
    """
    Generates a completed grid graph with a point on every vertex of the grid

    :param n: an int, the width of the grid in the graph
    :param m: an int, the height of the grid in the graph
    :return: a graph on a filled in grid of nodes with n * m vertices
    """
    graph = nx.DiGraph()
    #graph.add_nodes_from(range(n))
    points = []
    for k in range(n):
        for l in range(m):
            point = (k/n, l/m)
            points.append(point)
            graph.add_node(k*n+l, pos=point)
    # for each pair of nodes, calculate distance and add weighted edge
    graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                            + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                    for i, j in itertools.combinations(range(n*m), 2))
    graph.add_weighted_edges_from((j, i, ((points[i][0] - points[j][0]) ** 2
                                            + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                    for i, j in itertools.combinations(range(n*m), 2))
    return graph

def length_of_path(graph, path):
    """
    Calculates the length of a given path within a given graph

    :param graph: a nx.Graph to find the length of a path in
    :param path: a list of nodes (ints) giving the order of the path
    :return: a float, the length of the path within the graph
    """
    current = path[0]
    length = 0
    for nxt in path[1:]:
        length += graph[current][nxt]['weight']
        current = nxt
    return length
