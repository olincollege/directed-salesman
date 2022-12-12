import utils
import networkx as nx
import numpy as np
import branch_helpers as helpers

def branch_and_bound(graph):
    """
    
    """

    root = helpers.Root_Node(graph)
    sorted_active_nodes = [root]
    list_cap = 10
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

