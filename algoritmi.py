from itertools import permutations
import itertools
from functools import lru_cache

nodes = {
    "Munich": (300, 400),
    "Maribor": (100, 400),
    "Frankfurt": (100, 100),
    "Dunaj": (300, 100)
}

edges = [
    ("Munich", "Maribor", 467),
    ("Maribor", "Munich", 466),
    ("Maribor", "Frankfurt", 795),
    ("Frankfurt", "Maribor", 780),
    ("Frankfurt", "Dunaj", 718),
    ("Dunaj", "Frankfurt", 731),
    ("Frankfurt", "Munich", 396),
    ("Munich", "Frankfurt", 409),
    ("Dunaj", "Maribor", 253),
    ("Maribor", "Dunaj", 254),
    ("Dunaj", "Munich", 404),
    ("Munich", "Dunaj", 403)
]


def brute_force_tsp(nodes, edges):
    node_list = list(nodes.keys())
    all_permutations = itertools.permutations(node_list)
    shortest_path = None
    shortest_distance = float('inf')

    for perm in all_permutations:
        # Convert perm to a list and add the starting node at the end to complete the cycle
        current_path = list(perm) + [perm[0]]
        current_distance = total_distance(current_path, edges)
        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_path = current_path

    return shortest_path, shortest_distance


def Permutations_tsp(nodes, edges):
    node_list = list(nodes.keys())
    all_permutations = itertools.permutations(node_list)
    permutations_with_distances = []

    for perm in all_permutations:
        # Convert perm to a list and add the starting node at the end to complete the cycle
        current_path = list(perm) + [perm[0]]
        current_distance = total_distance(current_path, edges)
        permutations_with_distances.append((current_path, current_distance))

    return permutations_with_distances


def nearest_neighbor_tsp(nodes, edges, start_node):
    unvisited = set(nodes.keys())
    unvisited.remove(start_node)
    path = [start_node]
    current_node = start_node

    while unvisited:
        nearest_node = min(unvisited, key=lambda node: get_edge_distance(current_node, node, edges))
        path.append(nearest_node)
        current_node = nearest_node
        unvisited.remove(current_node)

    path.append(start_node)  # return to the start
    return path


def Dinamicni(nodes, edges):
    n = len(nodes)
    node_list = list(nodes.keys())
    all_distances = [[0] * n for _ in range(n)]

    # Fill the distance matrix
    for i in range(n):
        for j in range(n):
            if i != j:
                all_distances[i][j] = get_edge_distance(node_list[i], node_list[j], edges)

    @lru_cache(None)
    def dp(mask, pos):
        if mask == (1 << n) - 1:
            return all_distances[pos][0]
        min_cost = float('inf')
        for city in range(n):
            if mask & (1 << city) == 0:
                new_cost = all_distances[pos][city] + dp(mask | (1 << city), city)
                min_cost = min(min_cost, new_cost)
        return min_cost

    optimal_cost = dp(1, 0)

    # Reconstruct the path
    mask = 1
    pos = 0
    path = ["Munich"]
    for _ in range(n - 1):
        next_city = None
        min_cost = float('inf')
        for city in range(n):
            if mask & (1 << city) == 0:
                new_cost = all_distances[pos][city] + dp(mask | (1 << city), city)
                if new_cost < min_cost:
                    min_cost = new_cost
                    next_city = city
        path.append(node_list[next_city])
        mask |= (1 << next_city)
        pos = next_city
    path.append("Munich")

    return path, optimal_cost

def total_distance(path, edges):
    total_dist = 0
    for i in range(len(path) - 1):
        total_dist += get_edge_distance(path[i], path[i + 1], edges)
    return total_dist

def get_edge_distance(start, end, edges):
    for edge in edges:
        if edge[0] == start and edge[1] == end:
            return edge[2]
    return float('inf')  # if no direct edge exists
