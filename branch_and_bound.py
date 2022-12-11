import utils
import networkx as nx
import numpy as np
import branch_helpers as helpers

def branch_and_bound(graph):
    """
    
    """

    root = helpers.Root_Node(graph)
    size = graph.number_of_nodes()

    current_level_nodes = [root]
    while True:
        if len(current_level_nodes) == 0:
            break
        curr_min_cost = np.inf
        curr_min_nodes = []
        for node in current_level_nodes:
            if node.remaining_graph_nodes == []:
                break
            for x in node.remaining_graph_nodes:
                child = node.branch(x)
                if child.lower_bound < curr_min_cost:
                    curr_min_cost = child.lower_bound
                    curr_min_nodes = [child]
                elif child.lower_bound == curr_min_cost:
                    curr_min_nodes.append(child)
                else:
                    pass
        current_level_nodes = curr_min_nodes
    cost = node.lower_bound
    path = node.elapsed
    path.append(0)
    return cost, path

