import pygame
import sys
import math
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300
FPS = 60
BLACK = (0, 0, 0)
FONT_COLOR = (255, 255, 255)

# Colors for segments
SEGMENT_COLORS = [
    (255, 99, 71),    # Tomato
    (135, 206, 250),  # Light Sky Blue
    (255, 215, 0),    # Gold
    (144, 238, 144),  # Light Green
    (255, 182, 193),  # Light Pink
    (255, 165, 0),    # Orange
    (173, 216, 230),  # Light Blue
    (221, 160, 221),  # Plum
]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Wheel")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
result_font = pygame.font.SysFont(None, 48)

def draw_wheel(segments, angle):
    num_segments = len(segments)
    arc_angle = 360 / num_segments
    start_angle = angle

    for i, text in enumerate(segments):
        color = SEGMENT_COLORS[i % len(SEGMENT_COLORS)]
        # Draw segment
        pygame.draw.pie = draw_pie  # patch pygame to add draw_pie function
        draw_pie(screen, CENTER, RADIUS, math.radians(start_angle), math.radians(start_angle + arc_angle), color)
        # Draw text
        mid_angle = math.radians(start_angle + arc_angle / 2)
        text_x = CENTER[0] + (RADIUS / 2) * math.cos(mid_angle)
        text_y = CENTER[1] + (RADIUS / 2) * math.sin(mid_angle)
        text_surface = font.render(text, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)
        start_angle += arc_angle

def draw_pie(surface, center, radius, start_angle, end_angle, color):
    points = [center]
    step = math.radians(1)
    angle = start_angle
    while angle <= end_angle:
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
        angle += step
    # Ensure last point is exactly at end_angle
    x = center[0] + radius * math.cos(end_angle)
    y = center[1] + radius * math.sin(end_angle)
    points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def get_segment_index(angle, num_segments):
    # Normalize angle to [0, 360)
    angle = angle % 360
    arc_angle = 360 / num_segments
    index = int((360 - angle + arc_angle / 2) % 360 // arc_angle)
    return index

def main():
    # Get user input for segments
    print("Enter the text for the lucky wheel segments, separated by commas (e.g. Prize1, Prize2, Prize3):")
    input_text = input()
    segments = [s.strip() for s in input_text.split(",") if s.strip()]
    if len(segments) < 2:
        print("Please enter at least two segments.")
        sys.exit()

    angle = 0
    spinning = False
    spin_speed = 0
    result_text = ""
    show_result = False

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                mouse_pos = pygame.mouse.get_pos()
                dist = math.hypot(mouse_pos[0] - CENTER[0], mouse_pos[1] - CENTER[1])
                if dist <= RADIUS:
                    # Start spinning
                    spinning = True
                    spin_speed = random.uniform(15, 30)
                    show_result = False

        if spinning:
            angle += spin_speed
            spin_speed *= 0.97  # friction to slow down
            if spin_speed < 0.1:
                spinning = False
                spin_speed = 0
                # Determine result
                index = get_segment_index(angle, len(segments))
                result_text = f"Result: {segments[index]}"
                show_result = True

        draw_wheel(segments, angle)

        # Draw pointer
        pygame.draw.polygon(screen, (255, 0, 0), [(CENTER[0], CENTER[1] - RADIUS - 20), (CENTER[0] - 20, CENTER[1] - RADIUS + 10), (CENTER[0] + 20, CENTER[1] - RADIUS + 10)])

        if show_result:
            result_surface = result_font.render(result_text, True, (255, 255, 255))
            result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(result_surface, result_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
