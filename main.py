import pygame
import sys
import math
from button import Button
import itertools
from algoritmi import brute_force_tsp, Permutations_tsp, total_distance, nearest_neighbor_tsp, Dinamicni, branch_and_bound_tsp
from result import show_results, show_results_window

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (186, 85, 211)
BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traveling Salesman Problem")

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

AllPermsButton = Button("All permutations", (500, 50), (200, 50), GRAY, BLUE)
BruteForceButton = Button("Brute force", (525, 150), (150, 50), GRAY, BLUE)
NearestNeighbourButton = Button("Nearest Neighbour", (500, 250), (200, 50), GRAY, BLUE)
DinamicniButton = Button("Held-Karpov algoritem", (475, 350), (250, 50), GRAY, BLUE)
BranchAndBoundButton = Button("Branch and bound", (475, 450), (250, 50), GRAY, BLUE)



default_cursor = pygame.cursors.arrow
hover_cursor = pygame.cursors.tri_left

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if BruteForceButton.is_hovered():
                shortest_path, shortest_distance = brute_force_tsp(nodes, edges)
                print("Shortest path Brute force:", shortest_path)
                print("Shortest distance:", shortest_distance)
                print("________________________________________")
                show_results("Brute Force TSP Result", shortest_path, shortest_distance)
            elif AllPermsButton.is_hovered():
                all_permutations = Permutations_tsp(nodes, edges)
                for perm, distance in all_permutations:
                    print("Path:", perm, "Distance:", distance)
                print("_________________________________________")
                show_results_window(all_permutations)
            elif NearestNeighbourButton.is_hovered():
                shortest_path = nearest_neighbor_tsp(nodes, edges, "Frankfurt")
                shortest_distance = total_distance(shortest_path, edges)
                print("Shortest path Nearest neighbour:", shortest_path)
                print("Shortest distance:", shortest_distance)
                print("________________________________________")
                show_results("Nearest Neighbor TSP Result", shortest_path, shortest_distance)
            elif DinamicniButton.is_hovered():
                shortest_path, shortest_distance = Dinamicni(nodes, edges)
                print("Shortest path Held-Karpov:", shortest_path)
                print("Shortest distance:", shortest_distance)
                print("________________________________________")
                show_results("Held-Karpov TSP Result", shortest_path, shortest_distance)
            elif BranchAndBoundButton.is_hovered():
                shortest_path, shortest_distance = branch_and_bound_tsp(nodes, edges)
                print("Shortest path Branch and bound:", shortest_path)
                print("Shortest distance:", shortest_distance)
                print("________________________________________")
                show_results("Branch and bound TSP Result", shortest_path, shortest_distance)

    screen.fill(WHITE)

    for edge in edges:
        start_pos = nodes[edge[0]]
        end_pos = nodes[edge[1]]
        weight = edge[2]
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    for node, pos in nodes.items():
        pygame.draw.circle(screen, PURPLE, pos, 20)
        font = pygame.font.SysFont(None, 20)
        text = font.render(node, True, BLACK)
        if node in ["Frankfurt", "Dunaj"]:
            text_rect = text.get_rect(center=(pos[0], pos[1] - 30))
        else:
            text_rect = text.get_rect(center=(pos[0], pos[1] + 30))
        screen.blit(text, text_rect)

    BruteForceButton.draw(screen)
    NearestNeighbourButton.draw(screen)
    AllPermsButton.draw(screen)
    DinamicniButton.draw(screen)
    BranchAndBoundButton.draw(screen)

    if BruteForceButton.is_hovered() or AllPermsButton.is_hovered() or NearestNeighbourButton.is_hovered() or DinamicniButton.is_hovered():
        pygame.mouse.set_cursor(*hover_cursor)
    else:
        pygame.mouse.set_cursor(*default_cursor)

    pygame.display.flip()

pygame.quit()
sys.exit()
