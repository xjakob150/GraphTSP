from itertools import permutations
import itertools
from functools import lru_cache
import heapq

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


def branch_and_bound_tsp(nodes, edges):
    n = len(nodes)
    node_list = list(nodes.keys())
    all_distances = [[float('inf')] * n for _ in range(n)]

    # Fill the distance matrix
    for i in range(n):
        for j in range(n):
            if i != j:
                all_distances[i][j] = get_edge_distance(node_list[i], node_list[j], edges)

    # Priority queue to store the live nodes of the search tree
    pq = []

    # Initial lower bound for the root node
    def calculate_initial_bound():
        bound = 0
        for i in range(n):
            min1, min2 = float('inf'), float('inf')
            for j in range(n):
                if i != j:
                    if all_distances[i][j] <= min1:
                        min2 = min1
                        min1 = all_distances[i][j]
                    elif all_distances[i][j] < min2:
                        min2 = all_distances[i][j]
            bound += (min1 + min2)
        return bound / 2

    def calculate_bound(path, level):
        bound = calculate_initial_bound()
        if level == 1:
            return bound

        for i in range(level - 1):
            bound -= (min([all_distances[path[i]][j] for j in range(n) if j not in path[:i + 1]]) +
                      min([all_distances[path[i + 1]][j] for j in range(n) if j not in path[:i + 2]])) / 2
        return bound

    initial_bound = calculate_initial_bound()

    # Priority queue element: (bound, cost, level, path)
    heapq.heappush(pq, (initial_bound, 0, 1, [0]))

    final_path = None
    min_cost = float('inf')

    while pq:
        bound, cost, level, path = heapq.heappop(pq)

        if bound < min_cost:
            for i in range(n):
                if i not in path:
                    new_path = path + [i]
                    new_cost = cost + all_distances[path[-1]][i]
                    if level == n - 1:
                        new_cost += all_distances[i][0]
                        if new_cost < min_cost:
                            min_cost = new_cost
                            final_path = new_path + [0]
                    else:
                        new_bound = calculate_bound(new_path, level + 1)
                        if new_bound < min_cost:
                            heapq.heappush(pq, (new_bound, new_cost, level + 1, new_path))

    return [node_list[i] for i in final_path], min_cost