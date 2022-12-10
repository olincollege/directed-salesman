import networkx as nx

"""
Docstring placeholder
"""

def tsp_nearest_neighbor(graph):
    nx.draw(graph, nx.get_node_attributes(graph, 'pos'))
    solution_path = []
    seen = set()
    length = 0
    start_city = 0
    print(f"Len graph is {len(graph)}")
    print(f"start city is {start_city}")
    curr_city = start_city
    all_cities_visited = False
    solution_path.append(start_city)
    seen.add(start_city)
    print(f"Solution path is {solution_path}")
    while len(seen) < len(graph):
        # Find nearest unvisited city and make that current city - add to solution path
        nearest = find_nearest_city(curr_city, graph, seen)
        solution_path.append(nearest)
        seen.add(nearest)
        print(f"Solution path is {solution_path}")
        length += graph[curr_city][nearest]['weight']
        curr_city = nearest
    # Return to the start city once you have visited every city
    solution_path.append(start_city)
    length += graph[curr_city][start_city]['weight']
    # Return path
    print(f"The solution path is {solution_path}")
    return length, solution_path

"""
Docstring placeholder
"""

def find_nearest_city(curr_city_index, graph, solution_path) -> int:
    return min((i for i in range(len(graph)) if i not in solution_path), key=lambda i: graph[curr_city_index][i]['weight'])