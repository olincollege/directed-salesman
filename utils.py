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
        points = []
        for k in range(n):
            point = (random.random(), random.random())
            points.append(point)
            graph.add_node(k, pos=point)

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
        points = []
        for k in range(n):
            point = (random.random(), random.random())
            points.append(point)
            graph.add_node(k, pos=point)
        # for each pair of nodes, calculate distance and add weighted edge
        graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                              + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                      for i, j in itertools.combinations(range(n), 2))
    return graph

def barbell_graph(n: int) -> nx.Graph:
    """
    Generates a barbell graph with a total of n nodes

    :param n: the total number of nodes 
    """
    graph = nx.Graph()
    dist_between_ends = 5
    points = []
    left_points = n//2
    right_points = n - left_points
    for k in range(left_points):
        point = (random.random(), random.random())
        points.append(point)
        graph.add_node(k, pos=point)
    for h in range(right_points):
        point = (random.random() + dist_between_ends ** 0.5, random.random() + dist_between_ends ** 0.5)
        points.append(point)
        graph.add_node(h + left_points, pos=point)
    graph.add_weighted_edges_from((i, j, ((points[i][0] - points[j][0]) ** 2
                                              + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                      for i, j in itertools.combinations(range(left_points), 2))
    graph.add_weighted_edges_from((left_points + i, left_points + j, ((points[i][0] - points[j][0]) ** 2
                                              + (points[i][1] - points[j][1]) ** 2) ** 0.5)
                                      for i, j in itertools.combinations(range(right_points), 2))
    left_node = 1 - 1
    right_node = n - 1
    x_dist = points[left_node][0] - points[right_node][0]
    y_dist = points[left_node][1] - points[right_node][1]
    real_dist = (x_dist ** 2 + y_dist ** 2) ** 0.5
    graph.add_edge(0, right_node, weight=real_dist)
    
    return graph
                                     
def complete_barbell(n: int) -> nx.Graph:
    """
    Generates a "complete" barbell graph with a total of n nodes,
    so every node is connected but there's two distinct groups

    :param n: n total nodes
    """
    dist_between_ends = 5
    graph = nx.Graph()
    points = []
    left_points = n//2
    right_points = n - left_points
    for k in range(left_points):
        point = (random.random(), random.random())
        points.append(point)
        graph.add_node(k, pos=point)
    for h in range(right_points):
        point = (random.random() + dist_between_ends ** 0.5, random.random() + dist_between_ends ** 0.5)
        points.append(point)
        graph.add_node(h + left_points, pos=point)
    
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

def rectangle_graph(sizes: tuple, is_directed: bool = False) -> nx.Graph:
    """
    Generates a completed grid graph with a point on every vertex of the grid

    :param n: an int, the width of the grid in the graph
    :param m: an int, the height of the grid in the graph
    :return: a graph on a filled in grid of nodes with n * m vertices
    """
    n = min(sizes)
    m = max(sizes)
    graph = nx.DiGraph()
    #graph.add_nodes_from(range(n))
    points = []
    count = 0
    for k in range(n):
        for l in range(m):
            point = (k, l)
            points.append(point)
            graph.add_node(count, pos=point)
            count += 1
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


def create_adjacency_matrix(graph: nx.Graph):
    """
    Creates an adjacency matrix from the graph
    
    :param graph: a nx.Graph
    :return: numpy adjacency matrix of the given graph
    """
    return nx.adjacency_matrix(graph)
