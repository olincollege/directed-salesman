import networkx as nx

"""
    Runs the nearest neighbor algorithm on a given graph

    Finds the shortest path from 0 to last city by finding nearest node to
    the designated current city and adding that city to a set of visited 
    cities to ensure that no two cities are visited. 

    :param graph: the Graph to find the path through, with nodes labeled 0, 1, ...
    :return: a tuple, first the length of the path, and solution path / set of 
    ordered cities
    """

def tsp_nearest_neighbor(graph):
    #nx.draw(graph, nx.get_node_attributes(graph, 'pos'))
    solution_path = []
    seen = set()
    length = 0
    start_city = 0
    #print(f"Len graph is {len(graph)}")
    #print(f"start city is {start_city}")
    curr_city = start_city
    all_cities_visited = False
    solution_path.append(start_city)
    seen.add(start_city)
    #print(f"Solution path is {solution_path}")
    while len(seen) < len(graph):
        # Find nearest unvisited city and make that current city - add to solution path
        nearest = find_nearest_city(curr_city, graph, seen)
        solution_path.append(nearest)
        seen.add(nearest)
        #print(f"Solution path is {solution_path}")
        length += graph[curr_city][nearest]['weight']
        curr_city = nearest
    # Return to the start city once you have visited every city
    solution_path.append(start_city)
    length += graph[curr_city][start_city]['weight']
    # Return path
    #print(f"The solution path is {solution_path}")
    return length, solution_path

"""
    Calculates the nearest neighbor to a given node 

    Finds the minimum weight between a designated node and every other node /
    city in the graph. Does not check the weight between two cities if the
    second city is already in the set of visited cities. 

    :param curr_city_index: the index of the current city / node in the graph
    (graph is a dict with keys corresponding to city index)
    :param graph: the Graph to find the path through, with nodes labeled 0, 1, ...
    :param solution_path: set of all cities that have been visited / added
    to the path already
    :return: a tuple, first the length of the path, and solution path / set of 
    ordered cities
    """

def find_nearest_city(curr_city_index, graph, solution_path) -> int:
    return min((i for i in range(len(graph)) if i not in solution_path), key=lambda i: graph[curr_city_index][i]['weight'])