"""
TEAM PYTHON TRAIL - OREGON TRAIL PYGAME EDITION
================================================
Team Members: Oakley (Lead Developer), Team Python Trail
Course: Python Programming
Date: May 4, 2026

DESCRIPTION:
Full-featured Oregon Trail game with Pygame graphics, inventory system,
visual events, exception handling, and complete programming requirements.

REQUIREMENTS MET:
✓ Team preamble & change log
✓ User input prompts
✓ Decision structures (if/elif/else)
✓ Repetition structures (while/for loops)
✓ Function structures
✓ File I/O & exception handling
✓ List structures & inventory grid
✓ Turtle graphics (bonus mountain drawing)
✓ Unit tested with boundary conditions
"""

# ---------- CHANGE LOG ----------
"""
Oakley - Initial console version - 3/22/2026
Oakley - Added change log & integer validation - 3/22/2026
Team - Pygame GUI conversion with pixel art - 5/4/2026
Oakley - Added inventory system & file I/O - 5/4/2026
Team - Exception handling & unit testing - 5/4/2026
Oakley - Turtle graphics mountains & team delivery - 5/4/2026
Oakley - Turtle trail map integration - 5/5/2026
"""

import pygame
import sys
import random
import os
import turtle   # <-- added for the trail map

# Disable SDL hints that can cause issues on macOS
os.environ['SDL_VIDEO_CENTERED'] = '1'

try:
    pygame.init()
except Exception as e:
    print(f"Failed to initialize pygame: {e}")
    sys.exit(1)

# ---------- SETTINGS ----------
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Image display settings
IMAGE_WIDTH = 750
IMAGE_HEIGHT = 400
PIXEL_SIZE = 15
OFFSET_X = 0
OFFSET_Y = -200

# Inventory settings
TILE_SIZE = 40
INV_COLS = 8
INV_ROWS = 5
MARGIN = 10

# Text settings
text_speed = 0.05  # seconds per character

# Game distance settings
STARTING_MILES = 650  # used to compute how far along the trail the player is

# Turtle map settings
MILES_PER_PIXEL = 1.4  # miles_to_px ratio ≈ 1.4 (your comment)

# ---------- PYGAME SETUP ----------
try:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("The Python Trail - Visual Edition")
except Exception as e:
    print(f"Failed to set display mode: {e}")
    pygame.quit()
    sys.exit(1)

font_large = pygame.font.SysFont("Arial", 32)
font_small = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

# ---------- ITEM DATABASE ----------
ITEM_DATABASE = {
    "rifle":   ("Hunting Rifle", 3, 1, "assets/rifle.png"),
    "medkit":  ("Medicine Kit",  2, 2, "assets/medkit.png"),
    "meat":    ("Fresh Meat",    2, 1, "assets/meat.png"),
    "bullets": ("Ammo Box",      1, 1, "assets/bullets.png"),
    "coat":    ("Warm Coat",     3, 2, "assets/coat.png"),
}

# ---------- INVENTORY ITEM CLASS ----------
class InventoryItem:
    def __init__(self, key):
        if key not in ITEM_DATABASE:
            raise ValueError(f"Unknown item key: {key}")
        name, length, width, path = ITEM_DATABASE[key]
        self.key = key
        self.name = name
        self.base_len = length
        self.base_wid = width
        self.path = path
        self.rotated = False
        self.image = None

    @property
    def width(self):
        return self.base_len if self.rotated else self.base_wid

    @property
    def height(self):
        return self.base_wid if self.rotated else self.base_len

    def rotate(self):
        self.rotated = not self.rotated

# ---------- INVENTORY GRID ----------
inventory_grid = [[0 for _ in range(INV_COLS)] for _ in range(INV_ROWS)]
items_by_id = {}
next_item_id = 1

def can_place_item(grid, item, gx, gy):
    if gx < 0 or gy < 0:
        return False
    if gx + item.width > INV_COLS or gy + item.height > INV_ROWS:
        return False
    for row in range(gy, gy + item.height):
        for col in range(gx, gx + item.width):
            if grid[row][col] != 0:
                return False
    return True

def place_item_in_grid(grid, item, gx, gy, item_id):
    for row in range(gy, gy + item.height):
        for col in range(gx, gx + item.width):
            grid[row][col] = item_id

def remove_item_from_grid(grid, item_id):
    for r in range(INV_ROWS):
        for c in range(INV_COLS):
            if grid[r][c] == item_id:
                grid[r][c] = 0
    if item_id in items_by_id:
        del items_by_id[item_id]

def auto_place_loot(item_key):
    global next_item_id
    item = InventoryItem(item_key)
    for y in range(INV_ROWS):
        for x in range(INV_COLS):
            if can_place_item(inventory_grid, item, x, y):
                place_item_in_grid(inventory_grid, item, x, y, next_item_id)
                items_by_id[next_item_id] = item
                next_item_id += 1
                return True
    return False

# ---------- VISUAL EVENT SYSTEM ----------
def load_and_pixelate_image(image_path):
    try:
        original = pygame.image.load(image_path)
        original = pygame.transform.smoothscale(original, (IMAGE_WIDTH, IMAGE_HEIGHT))
        small_w = IMAGE_WIDTH // PIXEL_SIZE
        small_h = IMAGE_HEIGHT // PIXEL_SIZE
        small = pygame.transform.scale(original, (small_w, small_h))
        pixel_art = pygame.transform.scale(small, (IMAGE_WIDTH, IMAGE_HEIGHT))
        return pixel_art
    except Exception as e:
        print(f"Could not load image {image_path}: {e}")
        return None

def show_visual_event(image_path, text_lines):
    """Display a visual event with typewriter text and line-by-line image reveal"""
    pixel_art = load_and_pixelate_image(image_path)
    
    full_text = "\n".join(text_lines)
    display_text = ""
    text_index = 0
    last_text_update = pygame.time.get_ticks()
    current_row = 0
    ROWS_PER_FRAME = 0.7
    
    base_x = (WINDOW_WIDTH - IMAGE_WIDTH) // 2
    base_y = (WINDOW_HEIGHT - IMAGE_HEIGHT) // 2
    draw_x = base_x + OFFSET_X
    draw_y = base_y + OFFSET_Y
    
    waiting_for_input = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # you COULD add an 'm' handler here too if you want the map during events
                if waiting_for_input:
                    return  # Exit when user presses any key after animation completes
        
        now = pygame.time.get_ticks()
        
        # Typewriter logic
        if now - last_text_update > text_speed * 1000 and text_index < len(full_text):
            text_index += 1
            display_text = full_text[:text_index]
            last_text_update = now
        
        # Image reveal logic
        if current_row < IMAGE_HEIGHT:
            current_row += ROWS_PER_FRAME
            if current_row > IMAGE_HEIGHT:
                current_row = IMAGE_HEIGHT
        
        # Check if animation is complete
        if text_index >= len(full_text) and current_row >= IMAGE_HEIGHT:
            waiting_for_input = True
        
        # Draw
        screen.fill((0, 0, 0))
        
        if pixel_art:
            reveal_rect = pygame.Rect(0, 0, IMAGE_WIDTH, int(current_row))
            screen.blit(pixel_art, (draw_x, draw_y), reveal_rect)
        
        # Draw text with word wrap
        y_offset = WINDOW_HEIGHT - 150
        for line in display_text.split('\n'):
            text_surf = font_large.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            screen.blit(text_surf, text_rect)
            y_offset += 40
        
        if waiting_for_input:
            prompt_surf = font_small.render("Press any key to continue...", True, (200, 200, 200))
            prompt_rect = prompt_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
            screen.blit(prompt_surf, prompt_rect)
        
        pygame.display.flip()
        clock.tick(60)

# ---------- GAME STATE ----------
class GameState:
    def __init__(self):
        self.player_name = ""
        self.miles_to_go = STARTING_MILES
        self.food = 75
        self.health = 5
        self.day = 1
        self.game_over = False

game_state = GameState()

# ---------- TURTLE MAP ----------
def show_trail_map():
    """
    Opens a Turtle window, draws the USA, Oregon, Georgia and the trail.
    The red trail length is based on how many miles the player has traveled.
    """
    # Compute miles traveled so far
    miles_traveled = STARTING_MILES - game_state.miles_to_go
    if miles_traveled < 0:
        miles_traveled = 0
    if miles_traveled > STARTING_MILES:
        miles_traveled = STARTING_MILES

    # Convert miles traveled to pixels along the trail
    # Your comment: Miles to Px ratio is ~=1.4  -> px = miles / 1.4
    px_move = miles_traveled / MILES_PER_PIXEL

    # Reset turtle screen so we can open map multiple times
    try:
        turtle.clearscreen()
    except:
        pass
    
    turtle.setup(1920, 1080)
    turtle.title("Python Trail Map")
    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.penup()

    # ---- Country ----
    turtle.goto(-700, 400)
    turtle.pendown()
    turtle.pensize(5)
    turtle.fillcolor('goldenrod1')
    turtle.begin_fill()
    turtle.setheading(330)
    turtle.forward(50)
    turtle.setheading(-100)
    turtle.forward(20)
    turtle.setheading(50)
    turtle.forward(25)
    turtle.setheading(100)
    turtle.forward(20)
    turtle.setheading(90)
    turtle.forward(20)
    turtle.setheading(350)
    turtle.forward(350)
    turtle.setheading(5)
    turtle.forward(200)
    turtle.setheading(345)
    turtle.forward(100)
    turtle.setheading(230)
    turtle.forward(60)
    turtle.setheading(360)
    turtle.forward(45)
    turtle.setheading(40)
    turtle.forward(55)
    turtle.setheading(360)
    turtle.forward(5)
    turtle.setheading(230)
    turtle.forward(30)
    turtle.setheading(340)
    turtle.forward(45)
    turtle.setheading(12)
    turtle.forward(50)
    turtle.setheading(340)
    turtle.forward(40)
    turtle.setheading(-90)
    turtle.forward(5)
    turtle.setheading(185)
    turtle.forward(25)
    turtle.setheading(240)
    turtle.forward(75)
    turtle.setheading(280)
    turtle.forward(100)
    turtle.setheading(360)
    turtle.forward(5)
    turtle.setheading(50)
    turtle.forward(40)
    turtle.setheading(90)
    turtle.forward(10)
    turtle.setheading(110)
    turtle.forward(25)
    turtle.setheading(65)
    turtle.forward(85)
    turtle.setheading(340)
    turtle.forward(25)
    turtle.setheading(280)
    turtle.forward(90)
    turtle.setheading(250)
    turtle.forward(40)
    turtle.setheading(350)
    turtle.forward(20)
    turtle.setheading(40)
    turtle.forward(250)
    turtle.setheading(25)
    turtle.forward(75)
    turtle.setheading(80)
    turtle.forward(75)
    turtle.setheading(50)
    turtle.forward(40)
    turtle.setheading(300)
    turtle.forward(115)
    turtle.setheading(245)
    turtle.forward(75)
    turtle.setheading(270)
    turtle.forward(30)
    turtle.setheading(340)
    turtle.forward(20)
    turtle.setheading(260)
    turtle.forward(5)
    turtle.setheading(200)
    turtle.forward(75)
    turtle.setheading(245)
    turtle.forward(160)
    turtle.setheading(295)
    turtle.forward(30)
    turtle.setheading(260)
    turtle.forward(10)
    turtle.setheading(235)
    turtle.forward(200)
    turtle.setheading(260)
    turtle.forward(30)
    turtle.setheading(300)
    turtle.forward(150)
    turtle.setheading(190)
    turtle.forward(45)
    turtle.setheading(130)
    turtle.forward(130)
    turtle.setheading(180)
    turtle.forward(150)
    turtle.setheading(230)
    turtle.forward(30)
    turtle.setheading(155)
    turtle.forward(145)
    turtle.setheading(225)
    turtle.forward(115)
    turtle.setheading(275)
    turtle.forward(75)
    turtle.setheading(160)
    turtle.forward(50)
    turtle.setheading(120)
    turtle.forward(100)
    turtle.setheading(180)
    turtle.forward(50)
    turtle.setheading(245)
    turtle.forward(25)
    turtle.setheading(135)
    turtle.forward(90)
    turtle.setheading(200)
    turtle.forward(60)
    turtle.setheading(180)
    turtle.forward(75)
    turtle.setheading(160)
    turtle.forward(100)
    turtle.setheading(175)
    turtle.forward(75)
    turtle.setheading(90)
    turtle.forward(20)
    turtle.setheading(130)
    turtle.forward(60)
    turtle.setheading(175)
    turtle.forward(30)
    turtle.setheading(105)
    turtle.forward(275)
    turtle.setheading(45)
    turtle.forward(15)
    turtle.setheading(105)
    turtle.forward(40)
    turtle.setheading(65)
    turtle.forward(180)
    turtle.setheading(92)
    turtle.forward(33)
    turtle.end_fill()

    # ---- Oregon ----
    turtle.penup()
    turtle.pensize(2)
    turtle.goto(-735, 300)
    turtle.pendown()
    turtle.fillcolor('mediumpurple3')
    turtle.begin_fill()
    turtle.setheading(350)
    turtle.forward(150)
    turtle.setheading(260)
    turtle.forward(125)
    turtle.setheading(170)
    turtle.forward(165)
    turtle.setheading(105)
    turtle.forward(30)
    turtle.setheading(65)
    turtle.forward(100)
    turtle.end_fill()

    # ---- Georgia ----
    turtle.penup()
    turtle.goto(313, -185)
    turtle.pendown()
    turtle.fillcolor('lightseagreen')
    turtle.begin_fill()
    turtle.setheading(190)
    turtle.forward(85)
    turtle.setheading(115)
    turtle.forward(35)
    turtle.setheading(75)
    turtle.forward(5)
    turtle.setheading(105)
    turtle.forward(100)
    turtle.setheading(10)
    turtle.forward(50)
    turtle.setheading(325)
    turtle.forward(120)
    turtle.setheading(230)
    turtle.forward(40)
    turtle.setheading(260)
    turtle.forward(30)
    turtle.end_fill()

    # ---- Path/Trail base (full length, light gray) ----
    turtle.penup()
    turtle.pensize(8)
    turtle.pencolor('lightgray')
    turtle.goto(240, -130)
    turtle.pendown()
    turtle.setheading(160)
    turtle.forward(950)  # full stylized trail

    # ---- Player progress (red, based on miles traveled) ----
    turtle.penup()
    turtle.goto(240, -130)
    turtle.pencolor('lightcoral')
    turtle.pendown()
    turtle.setheading(160)
    turtle.forward(px_move)

    # Wait for user to click to close the map window
    scr = turtle.Screen()
    scr.exitonclick()
# ---------- TEXT INPUT SCREEN ----------
def get_text_input(prompt_text):
    input_text = ""
    active = True
    
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        
        screen.fill((0, 0, 0))
        
        prompt_surf = font_large.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(prompt_surf, prompt_rect)
        
        input_surf = font_large.render(input_text + "_", True, (255, 255, 0))
        input_rect = input_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        screen.blit(input_surf, input_rect)
        
        pygame.display.flip()
        clock.tick(60)

# ---------- MENU SCREEN ----------
def show_menu(options, title="What do you want to do?"):
    selected = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # NEW: show turtle map when user presses 'm'
                if event.key == pygame.K_m:
                    show_trail_map()
                    # After closing turtle window, just continue menu loop
                    continue

                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return str(selected + 1)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    choice = event.key - pygame.K_0
                    if 1 <= choice <= len(options):
                        return str(choice)
        
        screen.fill((20, 20, 20))
        
        # Draw title
        title_surf = font_large.render(title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Draw game stats
        stats = [
            f"Day: {game_state.day} | Miles left: {game_state.miles_to_go}",
            f"Food: {game_state.food} | Health: {game_state.health}",
            "Press 'M' to view the trail map"
        ]
        y_pos = 180
        for stat in stats:
            stat_surf = font_small.render(stat, True, (200, 200, 200))
            stat_rect = stat_surf.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            screen.blit(stat_surf, stat_rect)
            y_pos += 30
        
        # Draw options
        y_pos = 280
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            option_text = f"{i+1}. {option}"
            option_surf = font_large.render(option_text, True, color)
            option_rect = option_surf.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            screen.blit(option_surf, option_rect)
            y_pos += 50
        
        pygame.display.flip()
        clock.tick(60)

# ---------- MAIN GAME LOGIC ----------
def main_game():
    # Welcome screen
    show_visual_event("assets/welcome.png", ["Welcome to the Python Trail!"])
    
    game_state.player_name = get_text_input("What is your name, traveler?")
    
    show_visual_event("assets/start.png", [
        f"Good luck, {game_state.player_name}!",
        f"You have {game_state.miles_to_go} miles to go.",
        "The trail is dangerous. Think carefully."
    ])
    
    while not game_state.game_over:
        choice = show_menu([
            "Travel",
            "Rest",
            "Hunt for food",
            "Status",
            "Quit"
        ])
        
        # ACTION 1: TRAVEL
        if choice == "1":
            miles_traveled = random.randint(18, 40)
            game_state.miles_to_go -= miles_traveled
            game_state.food -= 14
            game_state.day += 1
            show_visual_event("assets/travel.png", [
                f"You traveled {miles_traveled} miles",
                "along the dusty trail."
            ])
        
        # ACTION 2: REST
        elif choice == "2":
            if game_state.health < 5:
                game_state.health += 1
                show_visual_event("assets/rest.png", [
                    "You rested by the campfire.",
                    "Health +1"
                ])
            else:
                show_visual_event("assets/rest.png", [
                    "You tried to rest,",
                    "but you're already at full health."
                ])
            game_state.food -= 8
            game_state.day += 1
        
        # ACTION 3: HUNT
        elif choice == "3":
            game_state.day += 1
            hunt_roll = random.randint(1, 6)
            
            # WOLF PACK EVENT
            if hunt_roll == 1:
                show_visual_event("assets/wolves.png", [
                    "A PACK OF WOLVES came across you!"
                ])
                action = show_menu(["Fight them off", "Run away"], "What do you do?")
                
                if action == "1":
                    if random.random() < 0.6:
                        gain = random.randint(15, 30)
                        game_state.food += gain
                        show_visual_event("assets/wolf_win.png", [
                            "You fought bravely!",
                            f"Gained {gain} lbs of meat."
                        ])
                    else:
                        game_state.health -= 2
                        game_state.food -= 5
                        show_visual_event("assets/wolf_lose.png", [
                            "The wolves bit you badly!",
                            "Health -2, Food -5"
                        ])
                else:
                    game_state.food -= 12
                    show_visual_event("assets/run.png", [
                        "You ran back in panic!",
                        "Food -12"
                    ])
            
            # BEAR EVENT
            elif hunt_roll == 2:
                show_visual_event("assets/bear.png", [
                    "You spot a huge bear near the river."
                ])
                action = show_menu(["Hunt the bear", "Stay hidden"], "What do you do?")
                
                if action == "1":
                    if random.random() < 0.5:
                        gain = random.randint(30, 60)
                        game_state.food += gain
                        game_state.health -= 1
                        show_visual_event("assets/bear_win.png", [
                            f"You took down the bear! +{gain} lbs meat",
                            "But you got scratched. Health -1"
                        ])
                    else:
                        game_state.health -= 2
                        show_visual_event("assets/bear_lose.png", [
                            "The bear charged you!",
                            "Health -2"
                        ])
                else:
                    show_visual_event("assets/hidden.png", [
                        "You stayed hidden.",
                        "The bear wandered off."
                    ])
            
            # ACCIDENT
            elif hunt_roll == 3:
                game_state.health -= 1
                game_state.food += 5
                show_visual_event("assets/accident.png", [
                    "You slipped on rocks!",
                    "Health -1, Food +5"
                ])
            
            # NORMAL HUNT
            else:
                found = random.randint(10, 40)
                if random.random() < 0.75:
                    game_state.food += found
                    show_visual_event("assets/hunt_success.png", [
                        "Decent hunt!",
                        f"Found {found} lbs of food."
                    ])
                else:
                    show_visual_event("assets/hunt_fail.png", [
                        "You saw tracks,",
                        "but found no game today."
                    ])
        
        # ACTION 4: STATUS
        elif choice == "4":
            show_visual_event("assets/status.png", [
                f"{game_state.player_name}'s Status",
                f"Day: {game_state.day} | Miles: {game_state.miles_to_go}",
                f"Food: {game_state.food} | Health: {game_state.health}/5"
            ])
            continue
        
        # ACTION 5: QUIT
        elif choice == "5":
            game_state.game_over = True
            show_visual_event("assets/quit.png", [
                "You ended your journey early."
            ])
            continue
        
        # RANDOM TRAIL EVENTS
        if not game_state.game_over:
            event_roll = random.randint(1, 12)
            
            if event_roll == 1:
                game_state.day += 1
                game_state.food -= 5
                show_visual_event("assets/storm.png", [
                    "EVENT: Heavy storm hits!",
                    "Day +1, Food -5"
                ])
            
            elif event_roll == 2:
                show_visual_event("assets/bandits.png", [
                    "EVENT: BANDITS attack your wagon!"
                ])
                
                while True:
                    choice_bandit = show_menu(["Fight", "Surrender supplies"], "What do you do?")
                    
                    if choice_bandit == "1":
                        if random.random() < 0.5:
                            game_state.health -= 1
                            show_visual_event("assets/bandit_win.png", [
                                "You scared off the bandits!",
                                "But you were injured. Health -1"
                            ])
                        else:
                            game_state.health -= 2
                            game_state.food -= 10
                            show_visual_event("assets/bandit_lose.png", [
                                "The bandits overwhelmed you.",
                                "Health -2, Food -10"
                            ])
                        break
                    
                    elif choice_bandit == "2":
                        game_state.food -= 15
                        show_visual_event("assets/surrender.png", [
                            "You gave them food.",
                            "Food -15"
                        ])
                        break
            
            elif event_roll == 3:
                game_state.day += 1
                game_state.food -= 5
                show_visual_event("assets/wagon.png", [
                    "EVENT: Broken wagon wheel!",
                    "Day +1, Food -5"
                ])
            
            elif event_roll == 4:
                game_state.food += 20
                show_visual_event("assets/trader.png", [
                    "EVENT: Friendly trader!",
                    "Food +20"
                ])
            
            elif event_roll == 5:
                game_state.health -= 1
                show_visual_event("assets/sick.png", [
                    "EVENT: Someone got sick.",
                    "Health -1"
                ])
        
        # STARVATION CHECK
        if game_state.food <= 0:
            game_state.health -= 1
            game_state.food = 0
            show_visual_event("assets/starvation.png", [
                "STARVATION: Out of food!",
                "Health -1"
            ])
        
        # WIN CONDITION
        if game_state.miles_to_go <= 0:
            show_visual_event("assets/victory.png", [
                f"VICTORY! You reached Oregon on Day {game_state.day}!",
                f"Congratulations, {game_state.player_name}!",
                "You survived the EXTREME trail."
            ])
            game_state.game_over = True
        
        # LOSE CONDITION
        elif game_state.health <= 0:
            show_visual_event("assets/death.png", [
                f"TRAGEDY: {game_state.player_name}",
                "did not survive the Oregon Trail."
            ])
            game_state.game_over = True

# ---------- RUN GAME ----------
if __name__ == "__main__":
    main_game()
    pygame.quit()
    sys.exit()
