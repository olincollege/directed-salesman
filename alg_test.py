"""
Tools for testing the time to run the different algorithms
on various types of graph of various sizes
"""

import time
import utils
import networkx as nx
import brute_force
import math

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

def get_min_length_brute_force(graph: nx.Graph) -> float:
    """
    Gets the length of the shortest path through the given graph that hits every node.

    Do not run for a graph with more than 10 nodes, 9 or fewer is preferable

    :param graph: an nx Graph to find the shortest length of

    :return: a float representing the length of the shortest path through the given graph
    """
    best_length, best_path = brute_force.brute_force(graph)
    return best_length

def get_min_length_of_circle(n: int) -> float:
    """
    Gets the length of the shortest path through a circle graph of n nodes.

    :param n: the number of nodes in the circle graph

    :return: a float representing the length of the shortest path through
    a circle graph of n nodes
    """
    length = n * 2 * math.sin(math.pi/n)
    return length

def get_min_length_of_grid(width: int, height: int) -> float:
    """
    Gets the length of the shortest path through a grid graph of the given width and height

    :param width: the number of nodes wide the desired grid graph is
    :param height: the number of nodes high the desired grid graph is

    :return: a float representing the length of the shortest path through
    a grid graph with the given parameters
    """
    if width == 1 or height == 1:
        return (max(width, height) - 1) * 2
    if width%2 == 0 or height%2 == 0:
        return width * height
    else:
        return width * height - 1 + math.sqrt(2)

def get_largest_factor(n: int) -> int:
    """
    Returns the greatest whole factor less than n
    """
    factor = n//2
    while True:
        if factor == 0:
            return -1
        if ((n / factor) % 1) == 0:
            return factor
        factor = factor - 1

def run_on_range_with_correct(graph_making_alg, algorithm, sizes):
    """
    
    """
    times = []
    correctnesses = []
    for size in sizes:
        graph = graph_making_alg(size)
        if graph_making_alg == utils.circle_graph:
            shortest_length = get_min_length_of_circle(size)
        elif graph_making_alg == utils.rectangle_graph:
            width = get_largest_factor(size)
            height = size / width
            shortest_length = get_min_length_of_grid(width, height)
        else:
            shortest_length = get_min_length_brute_force(graph)
        taken_time, correctness = run_on_determined_graph(graph, algorithm, shortest_length)
        times.append(taken_time)
        correctnesses.append(correctness)
    return times, correctnesses
        
def run_on_range_no_correct(graph_making_alg, algorithm, sizes):
    """
    
    """
    times = []
    for size in sizes:
        graph = graph_making_alg(size)
        taken_time = run_on_determined_graph_no_correctness(graph, algorithm)
        times.append(taken_time)
    return times

def run_multiple_on_range_with_correct(graph_making_alg, algorithm, sizes, num_runs):
    """
    
    """
    super_times = []
    super_correct = []
    for size in sizes:
        times = []
        corrs = []
        for run in range(num_runs):
            taken, corr = run_on_range_with_correct(graph_making_alg, algorithm, [size])
            taken = taken[0]
            corr = corr[0]
            times.append(taken)
            corrs.append(corr)
        avg_time = sum(times) / num_runs
        avg_corr = sum(corrs) / num_runs
        super_times.append(avg_time)
        super_correct.append(avg_corr)
    return super_times, super_correct

def run_multiple_on_range_no_correct(graph_making_alg, algorithm, sizes, num_runs):
    """
    
    """
    super_times = []
    for size in sizes:
        times = []
        for run in range(num_runs):
            taken = run_on_range_no_correct(graph_making_alg, algorithm, [size])
            taken = taken[0]
            times.append(taken)
        avg_time = sum(times) / num_runs
        super_times.append(avg_time)
    return super_times
    

