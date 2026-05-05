import pygame
import sys
import os

# Disable SDL hints that can cause issues on macOS
os.environ['SDL_VIDEO_CENTERED'] = '1'

try:
    pygame.init()
except Exception as e:
    print(f"Failed to initialize pygame: {e}")
    sys.exit(1)

# ---------- CONFIG ----------
TILE_SIZE = 40
INV_COLS = 8
INV_ROWS = 5
MARGIN = 10

WINDOW_WIDTH = INV_COLS * TILE_SIZE + MARGIN * 3
WINDOW_HEIGHT = INV_ROWS * TILE_SIZE + MARGIN * 3 + 90

try:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Tarkov-Style Inventory Demo")
except Exception as e:
    print(f"Failed to set display mode: {e}")
    pygame.quit()
    sys.exit(1)

font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

# ---------- ITEM DATABASE ----------
# key: (item_name, Length (height), Width, Picture_path)
ITEM_DATABASE = {
    "rifle":   ("Hunting Rifle", 3, 1, "/Users/rubenmartinez/Library/Mobile Documents/com~apple~CloudDocs/Python scripts/Rifle.png"),
    "medkit":  ("Medicine Kit",  2, 2, "assets/medkit.png"),
    "meat":    ("Fresh Meat",    2, 1, "assets/meat.png"),
    "bullets": ("Ammo Box",      1, 1, "assets/bullets.png"),
    "coat":    ("Warm Coat",     3, 2, "assets/coat.png"),
}

# ---------- INVENTORY ITEM ----------
class InventoryItem:
    def __init__(self, key):
        if key not in ITEM_DATABASE:
            raise ValueError(f"Unknown item key: {key}")
        name, length, width, path = ITEM_DATABASE[key]
        self.key = key
        self.name = name
        self.base_len = length   # height in cells
        self.base_wid = width    # width in cells
        self.path = path         # image path (can load later)
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

# ---------- GRID + CORE FUNCTIONS ----------
inventory_grid = [[0 for _ in range(INV_COLS)] for _ in range(INV_ROWS)]
items_by_id = {}
next_item_id = 1

def can_place_item(grid, item, gx, gy):
    """Check if item can be placed at grid cell (gx, gy)."""
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
    """Place item in grid at (gx, gy) with id item_id."""
    for row in range(gy, gy + item.height):
        for col in range(gx, gx + item.width):
            grid[row][col] = item_id

def remove_item_from_grid(grid, item_id):
    """Remove all cells belonging to item_id."""
    for r in range(INV_ROWS):
        for c in range(INV_COLS):
            if grid[r][c] == item_id:
                grid[r][c] = 0
    if item_id in items_by_id:
        del items_by_id[item_id]

def auto_place_loot(item_key):
    """Try to place a new item of type item_key. Return True if placed."""
    global next_item_id
    item = InventoryItem(item_key)
    for y in range(INV_ROWS):
        for x in range(INV_COLS):
            if can_place_item(inventory_grid, item, x, y):
                place_item_in_grid(inventory_grid, item, x, y, next_item_id)
                items_by_id[next_item_id] = item
                print(f"Auto-placed {item.name} with id {next_item_id} at ({x}, {y})")
                next_item_id += 1
                return True
    print("No room to auto-place loot!")
    return False

def clear_grid():
    global next_item_id
    for r in range(INV_ROWS):
        for c in range(INV_COLS):
            inventory_grid[r][c] = 0
    items_by_id.clear()
    next_item_id = 1

# ---------- DRAWING ----------
def draw_grid(surface):
    surface.fill((20, 20, 20))
    for y in range(INV_ROWS):
        for x in range(INV_COLS):
            cell_rect = pygame.Rect(
                MARGIN + x * TILE_SIZE,
                MARGIN + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(surface, (50, 50, 50), cell_rect)
            if inventory_grid[y][x] != 0:
                pygame.draw.rect(surface, (0, 160, 0), cell_rect.inflate(-4, -4))
            pygame.draw.rect(surface, (100, 100, 100), cell_rect, 1)

def draw_cursor(surface, gx, gy, item):
    color = (255, 255, 0) if can_place_item(inventory_grid, item, gx, gy) else (255, 0, 0)
    for row in range(gy, gy + item.height):
        for col in range(gx, gx + item.width):
            if 0 <= col < INV_COLS and 0 <= row < INV_ROWS:
                cell_rect = pygame.Rect(
                    MARGIN + col * TILE_SIZE,
                    MARGIN + row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(surface, color, cell_rect, 2)

def draw_ui(surface, current_item_key, cursor_x, cursor_y):
    name, length, width, _ = ITEM_DATABASE[current_item_key]
    lines = [
        f"Current item: {name} (L={length}, W={width})",
        "Arrows: move | R: rotate | Enter: place",
        "1-5: switch item | A: auto-place | C: clear | Esc: quit",
        f"Cursor: ({cursor_x}, {cursor_y})"
    ]
    for i, text in enumerate(lines):
        txt_surf = font.render(text, True, (255, 255, 255))
        surface.blit(
            txt_surf,
            (MARGIN, INV_ROWS * TILE_SIZE + MARGIN * 2 + i * 22)
        )

# ---------- MAIN LOOP SETUP ----------
item_keys = list(ITEM_DATABASE.keys())
current_index = 0
current_item_key = item_keys[current_index]
current_item = InventoryItem(current_item_key)

cursor_x, cursor_y = 0, 0

# ---------- MAIN LOOP ----------
running = True
while running:
    # Limit events processed per frame to prevent buildup
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break

        elif event.type == pygame.KEYDOWN:
            # Command+Q for Mac quit
            if event.key == pygame.K_q and (event.mod & pygame.KMOD_META):
                running = False
                break
            elif event.key == pygame.K_ESCAPE:
                running = False
                break

            elif event.key == pygame.K_LEFT:
                cursor_x = max(0, cursor_x - 1)
            elif event.key == pygame.K_RIGHT:
                cursor_x = min(INV_COLS - 1, cursor_x + 1)
            elif event.key == pygame.K_UP:
                cursor_y = max(0, cursor_y - 1)
            elif event.key == pygame.K_DOWN:
                cursor_y = min(INV_ROWS - 1, cursor_y + 1)

            elif event.key == pygame.K_r:
                current_item.rotate()

            elif event.key == pygame.K_RETURN:
                if can_place_item(inventory_grid, current_item, cursor_x, cursor_y):
                    global_id = next_item_id
                    place_item_in_grid(inventory_grid, current_item, cursor_x, cursor_y, global_id)
                    items_by_id[global_id] = current_item
                    next_item_id += 1
                else:
                    print("Cannot place item here.")

            elif event.key == pygame.K_c:
                clear_grid()

            elif event.key == pygame.K_a:
                auto_place_loot(current_item_key)

            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                idx = event.key - pygame.K_1
                if 0 <= idx < len(item_keys):
                    current_index = idx
                    current_item_key = item_keys[current_index]
                    current_item = InventoryItem(current_item_key)

    draw_grid(screen)
    draw_cursor(screen, cursor_x, cursor_y, current_item)
    draw_ui(screen, current_item_key, cursor_x, cursor_y)

    pygame.display.flip()
    
    # Use wait instead of tick for more efficient timing
    clock.tick(60)

# Clean exit - force pygame to quit
pygame.quit()
sys.exit()
