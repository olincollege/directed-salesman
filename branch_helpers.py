import numpy as np
import networkx as nx
from copy import copy

def make_diag_infinite(matrix):
    """
    Swaps the zeros on the default adjacency matrices for
    infinity to make branch and bound work correctly.

    param matrix: the adjacency matrix returned for an nx graph
    return: matrix but with the entries on the diagonal set to
    equal infinity
    """
    size = matrix.shape[1]
    for i in range(size):
        matrix[i,i] = np.inf
    return matrix

def reduce_matrix(matrix):
    """
    Reduces the matrix by the guidelines of the branch and bound
    algorithms (defined below)
    https://www.techiedelight.com/travelling-salesman-problem-using-branch-and-bound/
    Finds the minimum value of each row and reduces every value in
    each row by the row's minimum.
    Then, does the same for each column. 
    Keeps track of the minimum of each row and column and returns
    the sum of those minimums as well as the new matrix

    param matrix: the adjacency matrix (infinitized) for the working
    graph.
    
    return: 
    reduced_matrix, adjacency matrix (np array) reduced
    cost, sum of minimums

    NOTE: THIS IS N^2 AND A MAJOR CONTRIBUTOR TO TIME COMPLEXITY
    """
    size = matrix.shape[1]
    cost = 0
    for i in range(size):
        row = matrix[i, :]
        row_min = np.min(row)
        if row_min == np.inf:
            break
        row = row - row_min
        cost += row_min
        matrix[i,:] = row
    for j in range(size):
        col = matrix[:, j]
        col_min = np.min(col)
        if col_min == np.inf:
            break
        col = col - col_min
        cost += col_min
        matrix[:,j] = col
    reduced_matrix = matrix
    return reduced_matrix, cost

def make_updated_array_for_movement(array: np.array, origin: int, dest: int) -> np.array:
    """
    Sets all entries at the origin row, dest column, and dest, origin to infinity. Used
    for marking an edge as traveled (once an edge is traveled, the path will never again
    leave from that edge's origin vertex or arrive at its destination, so we can safely 
    remove them by weighting them so high they'll never be chosen). Additionally, we'll
    never go back the way we came, so we can set the edge going the opposite direction to
    infinity in the same manner.

    :param array: an np array, the current adjacency matrix that should be edited
    :param origin: the node representing the origin of the added edge
    :param dest: the node representing the destination of the added edge

    returns:
    :array: the original array with the appropriate locations set to infinity.
    """

    array[origin,:] = float("inf")
    array[:,dest] = float("inf")
    array[dest,origin] = float("inf")
    return array

def insert_node_in_sorted_list(sorted_list: list, node) -> list:
    """
    Inserts a node into a list of nodes sorted by their cost. Used by the node class
    to keep track of which nodes are the most promising and allow linear time retrieval
    of the most promising node.

    :param sorted_list: a list of nodes sorted by their cost
    :param node: the node to add

    returns:
    :list: the updated list of nodes
    """
    index = 0
    length = len(sorted_list)
    if sorted_list == []:
        return [node]
    while node.lower_bound > sorted_list[index].lower_bound:
        if (index + 1) == length:
            break
        index += 1
        

    sorted_list.insert(index, node)
    return sorted_list
    
class Path_node:
    """
    A node of the state space tree used for central storage in the branch and bound algorithm.
    The node represents the partial expansion of one path through the graph (and likewise) through
    the state space tree. 

    :param parent: the node representing the parent of this node
    :param next_node: the node of the higher-level graph that this path node represents the expansion to

    Fields:
    :parent: a path_node representing the parent of this node
    :parent_last: the last graph node the parent node touched
    :children: the children of this path node
    :remaining_graph_nodes: the graph nodes that the path so far has not touched
    :elapsed: the graph nodes that the path so far has touched
    :lower_bound: the "lower bound" of this path. Represents the lowest possible cost of any expansion of this path
    :adjacency_matrix: the adjacency matrix representing the current state of the graph. inaccessible paths have
    their weights replaced with infinity and rows and columns have been reduced as appropriate (see references for
    details)
    """
    def __init__(self, parent, next_node):
        self.parent = parent
        parent_elapsed = self.parent.get_elapsed()
        parent_remaining = copy(self.parent.get_remaining())
        parent_adj = self.parent.get_adj()
        self.parent_last = parent_elapsed[-1]
        self.children = []
        self.elapsed = parent_elapsed + [next_node]
        self.remaining_graph_nodes = parent_remaining
        self.remaining_graph_nodes.remove(next_node)
        parent_adjacency_matrix = copy(parent_adj)
        movement_cost = parent_adjacency_matrix[self.parent_last, next_node]
        infinitized_adj = make_updated_array_for_movement(parent_adjacency_matrix, self.parent_last, next_node)
        reduced, cost = reduce_matrix(infinitized_adj)
        self.lower_bound = self.parent.lower_bound + cost + movement_cost
        self.adjacency_matrix = reduced
    
    def __str__(self):
        par_string = str(self.parent)
        children_string = str(self.children)
        elapsed_string = str(self.elapsed)
        remaining_string = str(self.remaining_graph_nodes)
        lower_bound_string = str(self.lower_bound)
        adj_mat_string = str(self.adjacency_matrix)
        print_string = f"children: {children_string}\nelapsed: {elapsed_string}\nadj mat: \n{adj_mat_string}\nlower bound: {lower_bound_string}\nremaining graph nodes: {remaining_string}"
        return print_string
    
    def branch(self, node):
        """
        Makes a new path node with this as the parent and going to graph node "node"
        """
        vertex = Path_node(self, node)
        self.children.append(vertex)
        return vertex
    def get_elapsed(self):
        """
        Simple getter
        """
        return self.elapsed
    def get_remaining(self):
        """
        Simple getter
        """
        return self.remaining_graph_nodes
    def get_adj(self):
        """
        Simple getter
        """
        return self.adjacency_matrix
    def has_nodes_remaining(self):
        """
        Simple boolean checking if there's any graph nodes left to explore
        """
        if len(self.remaining_graph_nodes) == 0:
            return False
        return True

class Root_Node:
    """
    Functionally the same as the path node but slightly different initialization
    """
    def __init__(self, graph: nx.Graph):
        self.children = []
        self.elapsed = [0]
        self.remaining_graph_nodes = list(graph.nodes)
        self.remaining_graph_nodes.remove(0)
        initial_adj = nx.to_numpy_matrix(graph)
        infinitized = make_diag_infinite(initial_adj)
        reduced, cost = reduce_matrix(infinitized)
        self.adjacency_matrix = reduced
        self.lower_bound = cost
    
    def __str__(self):
        children_string = str(self.children)
        elapsed_string = str(self.elapsed)
        remaining_string = str(self.remaining_graph_nodes)
        lower_bound_string = str(self.lower_bound)
        adj_mat_string = str(self.adjacency_matrix)
        print_string = f"children: {children_string}\nelapsed: {elapsed_string}\nadj mat: \n{adj_mat_string}\nlower bound: {lower_bound_string}\nremaining graph nodes: {remaining_string}"
        return print_string
    
    def branch(self, node):
        vertex = Path_node(self, node)
        self.children.append(vertex)
        return vertex

    def get_elapsed(self):
        return self.elapsed
    def get_remaining(self):
        return self.remaining_graph_nodes
    def get_adj(self):
        return self.adjacency_matrix
    def has_nodes_remaining(self):
        if len(self.remaining_graph_nodes) == 0:
            return False
        return True

