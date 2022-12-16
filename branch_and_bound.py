import utils
import networkx as nx
import numpy as np
import branch_helpers as helpers

def branch_and_bound(graph: nx.Graph):
    """
    Takes an input graph, uses a branch and bound algorithm to find the shortest path throgh
    the graph that touches every vertex once, and returns the cost of that path plus the path 
    itself. Uses a bounding strategy of only keeping the [list_cap] most promising nodes to consider.

    :param graph: An nx graph to be evaluated

    returns:
    :cost: a float representing the "cost" of this path through the graph. The sum of all edges taken.
    :path: a list of ints representing the ordered path the solution takes through the graph.

    Time complexity average O(n^3):
     - n from expanding nodes on the order of O(n) (maybe 2n, maybe 3n but still order n)
     - n^2 from reducing the adjacency matrix (of every node so we multiply). Adj_mat is of size n^2
     so reducing is of order O(n^2)
    Multiply to get O(n^3) for cases where the number of path nodes expanded is proportional to the number 
    of nodes in the graph.

    Time complexity worst O(n!):
     - if we expand all or most path nodes, we expand path nodes on the order of n!
     - n^2 to reduce adjacency matrix like before but that's subsumed into the factorial so we can ignore
    """

    root = helpers.Root_Node(graph)
    sorted_active_nodes = [root]
    list_cap = 20
    while True:
        node = sorted_active_nodes[0]
        if node.remaining_graph_nodes == []:
            break
        sorted_active_nodes.pop(0)
        if node.remaining_graph_nodes != []:
            for x in node.remaining_graph_nodes:
                child = node.branch(x)
                sorted_active_nodes = helpers.insert_node_in_sorted_list(sorted_active_nodes, child)
        if len(sorted_active_nodes) >= list_cap:
            sorted_active_nodes = sorted_active_nodes[:list_cap]
    
    cost = node.lower_bound
    path = node.elapsed
    path.append(0)
    return cost, path

