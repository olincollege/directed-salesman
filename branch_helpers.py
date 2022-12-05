import numpy as np

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
        matrix[i,i] = float("inf")
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
    """
    size = matrix.shape[1]
    cost = 0
    for i in range(size):
        row = matrix[i, :]
        row_min = row.min()
        row = row - row_min
        cost += row_min
        matrix[i,:] = row
    for j in range(size):
        col = matrix[:, j]
        col_min = col.min()
        col = col - col_min
        cost += col_min
        matrix[:,j] = col
    reduced_matrix = matrix
    return reduced_matrix, cost


class Tree:
    """
    A tree to hold the possible paths through 
    """
    def __init__(self, root, graph_nodes):
        self.root = root
        self.graph_nodes = graph_nodes

class Path_node:
    def __init__(self, parent, children, graph_node, adjacency_matrix, tree, cost):
        self.parent = parent
        self.children = children
        self.graph_node = graph_node
        self.adjacency_matrix = adjacency_matrix
        self.tree = tree
        self.cost = cost
        if self.parent is None:
            self.remaining_graph_nodes = self.tree.graph_nodes
        else: 
            print(self.parent)
            par = self.parent
            self.remaining_graph_nodes = par.remaining_graph_nodes
        self.remaining_graph_nodes.remove(self.graph_node)
    
    def __str__(self):
        par_string = str(self.parent)
        children_string = str(self.children)
        graph_node_string = str(self.graph_node)
        adj_mat_string = str(self.adjacency_matrix)
        cost_string = str(self.cost)
        rem_graph_node_string = str(self.remaining_graph_nodes)
        print_string = f"parent: {par_string}\nchildren: {children_string}\ngraph_node: {graph_node_string}\nadj mat: \n{adj_mat_string}\ncost: {cost_string}\nremaining graph nodes: {rem_graph_node_string}"
        return print_string
    