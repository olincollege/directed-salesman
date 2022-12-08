import utils
import networkx as nx
import numpy as np
import branch_helpers as helpers

def branch_and_bound(graph):
    """
    
    """

    root = helpers.Root_Node(graph)
    size = graph.number_of_nodes()

    limit_reached = False
    current_level_nodes = [root]
    for _ in range(size - 1):
        curr_min_cost = np.inf
        curr_min_nodes = []
        for node in current_level_nodes:
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
    cost = current_level_nodes[0].lower_bound
    path = current_level_nodes[0].elapsed
    path.append(0)
    return cost, path