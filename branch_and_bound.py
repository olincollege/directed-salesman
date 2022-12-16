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

