import pygame
import sys

# ---------- SETTINGS ----------
IMAGE_PATH = r"/Users/rubenmartinez/Library/Mobile Documents/com~apple~CloudDocs/Python scripts/chapter 7/picture-24.png"

# Window size
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 800

# Image size and position
IMAGE_WIDTH  = 750
IMAGE_HEIGHT = 400
PIXEL_SIZE = 15

OFFSET_X = 0
OFFSET_Y = -200   # move image up a bit so there's room for text at bottom

# --- Typewriter text settings ---
full_text = "Off in the distance it appears as if there \n is a group of bandits coming at you?"
display_text = ""
text_index = 0
text_speed = 0.1  # seconds per character
last_text_update = pygame.time.get_ticks()

# --- Line-by-line reveal settings ---
ROWS_PER_FRAME = .7  # how many horizontal rows appear each frame
current_row = 4     # start with 0 rows visible

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixel Portrait + Typewriter Text")
font = pygame.font.SysFont("Arial", 32)
clock = pygame.time.Clock()

# ---------- LOAD & PIXELATE IMAGE ----------
try:
    original = pygame.image.load(IMAGE_PATH)
except Exception as e:
    print("Could not load image:", e)
    pygame.quit()
    sys.exit()

# 1) Scale original to our rectangle size
original = pygame.transform.smoothscale(original, (IMAGE_WIDTH, IMAGE_HEIGHT))

# 2) Shrink for pixelation
small_w = IMAGE_WIDTH  // PIXEL_SIZE
small_h = IMAGE_HEIGHT // PIXEL_SIZE
small = pygame.transform.scale(original, (small_w, small_h))

# 3) Blow it back up (each tiny pixel becomes a block)
pixel_art = pygame.transform.scale(small, (IMAGE_WIDTH, IMAGE_HEIGHT))

# Centering math with offsets
base_x = (WINDOW_WIDTH  - IMAGE_WIDTH)  // 2
base_y = (WINDOW_HEIGHT - IMAGE_HEIGHT) // 2
draw_x = base_x + OFFSET_X
draw_y = base_y + OFFSET_Y

# ---------- MAIN LOOP ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- TYPEWRITER LOGIC ----
    now = pygame.time.get_ticks()
    if now - last_text_update > text_speed * 1000 and text_index < len(full_text):
        text_index += 1
        display_text = full_text[:text_index]
        last_text_update = now

    # ---- IMAGE REVEAL LOGIC (line by line) ----
    if current_row < IMAGE_HEIGHT:
        current_row += ROWS_PER_FRAME
        if current_row > IMAGE_HEIGHT:
            current_row = IMAGE_HEIGHT

    # ---------- DRAW ----------
    screen.fill("black")  # black background

    # Draw only the top part of the image (from row 0 down to current_row)
    reveal_rect = pygame.Rect(0, 0, IMAGE_WIDTH, current_row)
    screen.blit(pixel_art, (draw_x, draw_y), reveal_rect)

    # Draw the typewriter text near the bottom
    text_surf = font.render(display_text, True, "white")
    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
    screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
