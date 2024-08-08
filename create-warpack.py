import json
import random

GRID_WIDTH = 9
GRID_HEIGHT = 7

class Item:
    def __init__(self, name, category, width, height, rotation):
        self.name = name
        self.category = category
        self.width = width
        self.height = height
        self.rotation = rotation

    def get_occupied_cells(self, start_x, start_y):
        occupied_cells = []
        if self.rotation == 0:
            for x in range(start_x, start_x + self.width):
                for y in range(start_y, start_y + self.height):
                    occupied_cells.append((x, y))
        elif self.rotation == -90:
            for x in range(start_x, start_x - self.height, -1):
                for y in range(start_y, start_y + self.width):
                    occupied_cells.append((x, y))
        # Add more rotations if needed
        return occupied_cells

def load_items(filename):
    with open(filename, 'r') as file:
        items_data = json.load(file)
    return [Item(**item) for item in items_data]

def is_placeable(grid, item, start_x, start_y):
    for x, y in item.get_occupied_cells(start_x, start_y):
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or grid[y][x] is not None:
            return False
    return True

def place_item(grid, item, start_x, start_y):
    for x, y in item.get_occupied_cells(start_x, start_y):
        grid[y][x] = item.name

def print_grid(grid):
    for row in grid:
        print(' '.join(['.' if cell is None else cell[0] for cell in row]))

def main():
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    items = load_items('items.json')

    for item in items:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            start_x = random.randint(0, GRID_WIDTH - 1)
            start_y = random.randint(0, GRID_HEIGHT - 1)
            if is_placeable(grid, item, start_x, start_y):
                place_item(grid, item, start_x, start_y)
                placed = True
            attempts += 1

    print_grid(grid)

if __name__ == "__main__":
    main()