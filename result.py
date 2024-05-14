import pygame
import math
import sys
import time
from button import Button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (186, 85, 211)
BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 155, 0)

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

Back = Button("Go back", (575, 100), (150, 50), GRAY, BLUE)

def draw_arrow(screen, start_pos, end_pos, line_color, arrow_color, arrow_size=10):
    # Calculate angle and arrowhead points
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    angle += math.pi  # Reverse angle for proper orientation
    arrow1 = (end_pos[0] + arrow_size * math.cos(angle - math.pi / 6),
              end_pos[1] + arrow_size * math.sin(angle - math.pi / 6))
    arrow2 = (end_pos[0] + arrow_size * math.cos(angle + math.pi / 6),
              end_pos[1] + arrow_size * math.sin(angle + math.pi / 6))

    # Draw line and arrowhead
    pygame.draw.line(screen, line_color, start_pos, end_pos, 2)
    pygame.draw.line(screen, line_color, end_pos, arrow1, 2)
    pygame.draw.line(screen, line_color, end_pos, arrow2, 2)
    pygame.draw.polygon(screen, arrow_color, [end_pos, arrow1, arrow2])

def show_results(window_title, path, distance):
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    result_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(window_title)

    running_result = True
    while running_result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_result = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Back.is_hovered():
                    running_result = False

        result_screen.fill(WHITE)

        for edge in edges:
            start_pos = nodes[edge[0]]
            end_pos = nodes[edge[1]]
            pygame.draw.line(result_screen, BLACK, start_pos, end_pos, 2)

        # Get the starting node from the path
        starting_node = path[0] if path else None

        for node, pos in nodes.items():
            color = GREEN if node == starting_node else PURPLE  # Use GREEN color for the starting node
            pygame.draw.circle(result_screen, color, pos, 20)
            font = pygame.font.SysFont(None, 20)
            text = font.render(node, True, BLACK)
            if node in ["Frankfurt", "Dunaj"]:
                text_rect = text.get_rect(center=(pos[0], pos[1] - 30))
            else:
                text_rect = text.get_rect(center=(pos[0], pos[1] + 30))
            result_screen.blit(text, text_rect)


        if path:
            for i in range(len(path) - 1):
                start_pos = nodes[path[i]]
                end_pos = nodes[path[i + 1]]
                draw_arrow(result_screen, start_pos, end_pos, BLUE, RED)  # Pass arrow color as an argument
            start_pos = nodes[path[-1]]
            end_pos = nodes[path[0]]
            draw_arrow(result_screen, start_pos, end_pos, BLUE, RED)  # Pass arrow color as an argument

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Total Distance: {distance} Km", True, BLACK)
        result_screen.blit(text, (20, 20))

        Back.draw(result_screen)

        pygame.display.flip()

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def show_results_window(results):
    result_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("All Permutations Result")

    running_result = True
    while running_result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_result = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Back.is_hovered():
                    running_result = False

        result_screen.fill(WHITE)

        # Display results
        font = pygame.font.SysFont(None, 20)
        y_offset = 50
        for perm, distance in results:
            text = font.render(f"Path: {perm}, Distance: {distance}", True, BLACK)
            result_screen.blit(text, (20, y_offset))
            y_offset += 20

        Back.draw(result_screen)

        pygame.display.flip()

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

default_cursor = pygame.cursors.arrow
hover_cursor = pygame.cursors.tri_left
