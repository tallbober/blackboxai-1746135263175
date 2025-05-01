import math
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300
BACKGROUND_COLOR = (0, 0, 0)
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

# Sample segments
segments = ["Prize 1", "Prize 2", "Prize 3", "Prize 4", "Prize 5", "Prize 6", "Prize 7", "Prize 8"]

def draw_pie(draw, center, radius, start_angle, end_angle, color):
    # Draw a pie slice as a polygon
    points = [center]
    step = 1  # degrees
    angle = start_angle
    while angle <= end_angle:
        rad = math.radians(angle)
        x = center[0] + radius * math.cos(rad)
        y = center[1] + radius * math.sin(rad)
        points.append((x, y))
        angle += step
    # Ensure last point is exactly at end_angle
    rad = math.radians(end_angle)
    x = center[0] + radius * math.cos(rad)
    y = center[1] + radius * math.sin(rad)
    points.append((x, y))
    draw.polygon(points, fill=color)

def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    num_segments = len(segments)
    arc_angle = 360 / num_segments
    start_angle = 0

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    for i, text in enumerate(segments):
        color = SEGMENT_COLORS[i % len(SEGMENT_COLORS)]
        draw_pie(draw, CENTER, RADIUS, start_angle, start_angle + arc_angle, color)

        # Draw text
        mid_angle = math.radians(start_angle + arc_angle / 2)
        text_x = CENTER[0] + (RADIUS / 2) * math.cos(mid_angle)
        text_y = CENTER[1] + (RADIUS / 2) * math.sin(mid_angle)
        text_size = draw.textbbox((0, 0), text, font=font)
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]
        draw.text((text_x - text_width / 2, text_y - text_height / 2), text, fill=FONT_COLOR, font=font)

        start_angle += arc_angle

    # Draw pointer
    pointer = [(CENTER[0], CENTER[1] - RADIUS - 20), (CENTER[0] - 20, CENTER[1] - RADIUS + 10), (CENTER[0] + 20, CENTER[1] - RADIUS + 10)]
    draw.polygon(pointer, fill=(255, 0, 0))

    # Save image
    image.save("lucky_wheel_preview.png")
    print("Preview image saved as lucky_wheel_preview.png")

if __name__ == "__main__":
    main()
