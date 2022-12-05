"""
Tools for testing the time to run the different algorithms
on various types of graph of various sizes
"""

import time
import utils
import networkx as nx

def run_on_determined_graph(graph: nx.Graph, algorithm, shortest_length: float) -> [float, float]:
    """
    Runs the given algorithm on a complete circle graph of size n
    and returns the time taken to run that algorithm and the correctness
    of the algorithm


    :param graph: the networkx graph to run the algorithm on
    :param algorithm: the function for the algorithm (developed by us or not)
    :param shortest_length: the length of the true shortest path

    :return: a tuple of the time required to run the algorithm and the correctness
    of the solution (where 1 is exactly the shortest path and lower is worse)
    """
    
    start_time = time.time()
    best_length, best_path = algorithm(graph)
    end_time = time.time()
    taken_time = end_time - start_time
    correctness = shortest_length / best_length
    return taken_time, correctness

def run_on_determined_graph_no_correctness(graph: nx.Graph, algorithm) -> float:
    """
    Runs the given algorithm on a complete circle graph of size n
    and returns the time taken to run that algorithm and the correctness
    of the algorithm


    :param graph: the networkx graph to run the algorithm on
    :param algorithm: the function for the algorithm (developed by us or not)

    :return: a float representing the time required to run the algorithm
    """
    
    taken_time, correctness = run_on_determined_graph(graph, algorithm, 1)
    return taken_time

def run_on_generated_graph(graph_making_alg, algorithm, graph_size_args, shortest_length: float ) -> [float, float]:
    """
    Runs the given algorithm on a complete circle graph of size n
    and returns the time taken to run that algorithm and the correctness
    of the algorithm


    :param graph_making_alg: the function for which graph type to generate
    :param algorithm: the function for the algorithm (developed by us or not)
    :param graph_size_args: the argument to the graph making algorithm
    (int for random and circle, tuple of two ints for rectangle)
    :param shortest_length: the length of the true shortest path

    :return: a tuple of the time required to run the algorithm and the correctness
    of the solution (where 1 is exactly the shortest path and lower is worse)
    """
    
    graph = graph_making_alg(graph_size_args)
    taken_time, correctness = run_on_determined_graph(graph, algorithm, shortest_length)
    return taken_time, correctness

def run_on_generated_graph_no_correctness(graph_making_alg, algorithm, graph_size_args) -> float:
    """
    Runs the given algorithm on a complete circle graph of size n
    and returns the time taken to run that algorithm

    :param graph_making_alg: the function for which graph type to generate
    :param algorithm: the function for the algorithm (developed by us or not)
    :param graph_size_args: the argument to the graph making algorithm
    (int for random and circle, tuple of two ints for rectangle)

    :return: a float representing the time required to run the algorithm
    """

    graph = graph_making_alg(graph_size_args)
    taken_time = run_on_determined_graph_no_correctness(graph, algorithm)
    return taken_time