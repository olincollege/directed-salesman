import networkx as nx
from typing import *
import random
from utils import random_graph, create_adjacency_matrix

def dp_runner(i, bitmask, distance_matrix):
    """
    Traverses the graph and finds the shortest Hamiltonian path on a graph 
    using dynamic programming by caching inner paths to find most optimal path

    :i: ith node
    :bitmask: represents the remaining nodes in the subset (TODO: bits are faster to operate)

    :returns: cost of the most efficient path
    """
    n = len(distance_matrix)

    # Memoize for top down recursion
    cache = [[-1]*(1 << (n)) for _ in range(n)]
    
    # Base case: 
    # if only ith bit and 1st bit is set in our bitmask
    # we have visited all other nodes already
    if bitmask == ((1 << i) | 3):
        return distance_matrix[1][i]
  
    # Memoize visited distances
    if cache[i][bitmask] != -1:
        return cache[i][bitmask]
    
    # Result of the sub-problem
    result = 10**9
  
    # Travel to all nodes j and end the path at ith node
    for j in range(1, n):
        if (bitmask & (1 << j)) != 0 and j != i and j != 1:
            result = min(result, dp_runner(j, bitmask & (~(1 << i)), distance_matrix) + distance_matrix[j][i])
    
    # Store minimum value
    cache[i][bitmask] = result
    return result

def dp(graph: nx.Graph) -> Tuple[float, List[int]]:
    """
    Implementation and testing of a DP-based TSP Search algorithm

    :param graph: a graph of unspecified type and `n` nodes

    """

    best_length = 10**9
    best_path = []

    # Get number of nodes for cache
    n = graph.number_of_nodes()

    # Turn graph into distance matrix
    adj_graph = create_adjacency_matrix(graph)
    graph_matrix = adj_graph.todense().tolist()

    # Go from node 1 visiting all nodes in between to i
    # Return to i when complete
    for i in range(1, n):
        best_length = min(best_length, dp_runner(i, (1 << n)-1, graph_matrix) + graph_matrix[i][1])
        best_path.append(graph_matrix[1][i])

    return best_length, best_path
