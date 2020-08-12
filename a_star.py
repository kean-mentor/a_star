import queue
import sys

import pygame

from colors import GREY, WHITE
from constants import CellType, HEIGHT, WIDTH, SIZE
from spot import Spot


# Some PyGame init code
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("A* Pathfinding Algorithm")
surface = pygame.display.set_mode((WIDTH, HEIGHT))


def prepare_cell_data():
    rows = HEIGHT // SIZE
    cols = WIDTH // SIZE
 
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            spot = Spot(r, c)
            grid[r].append(spot)

    return grid


def draw_cells(win, grid):
    for row in grid:
        for spot in row:
            spot.draw(win)

def draw_gridlines(win):
    rows = HEIGHT // SIZE
    cols = WIDTH // SIZE

    for r in range(rows):
        pygame.draw.line(win, GREY, (0, r * SIZE), (WIDTH, r * SIZE))
    for c in range(cols):
        pygame.draw.line(win, GREY, (c * SIZE, 0), (c * SIZE, HEIGHT))

def draw(win, grid):
    win.fill(WHITE)
    draw_cells(win, grid)
    draw_gridlines(win)

    pygame.display.update()


def get_clicked_cell(m_pos):
    row = m_pos[1] // SIZE
    col = m_pos[0] // SIZE
    return row, col


def reset_grid():
    print("Not implemented yet...")


def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        current = came_from[current]
        current.celltype = CellType.PATH
        draw_func()

def calculate_shortest_path(draw_func, grid, start, end):
    """https://en.wikipedia.org/wiki/A*_search_algorithm"""

    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}
    came_from = {}

    # g_score: Distance from start to current node
    g_score = {spot: float("inf") for row in grid for spot in row}  # TODO: Using objects as dict keys, is it OK?
    g_score[start] = 0
    # f_score: Sum of g_score and ESTIMATED distance from current to end node
    f_score = {spot: float("inf") for row in grid for spot in row}  # TODO: Using objects as dict keys, is it OK?
    f_score[start] = start.distance(end)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, current, draw_func)

            start.celltype = CellType.START
            end.celltype = CellType.END
            return True

        for neighbor in current.neighbors:
            new_g_score = g_score[current] + 1  # All edges are weighted equally
            # If this path to neighbor is better than any previous one. Record it!
            if new_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = new_g_score
                f_score[neighbor] = g_score[neighbor] + neighbor.distance(end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.celltype = CellType.OPEN

        draw_func()
        
        if current != start:
            current.celltype = CellType.CLOSED

    return False


grid = prepare_cell_data()
start = None  # Start point
end = None  # Destination point
is_started = False  # Pathfinding algorithm started or not
is_drawing = False  # Start and destination points are placed and left mouse button is pressed
is_running = True


while is_running:
    draw(surface, grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            continue
        if is_started:
            continue  # After the algorithm is started you can't modify the grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_clicked_cell(pygame.mouse.get_pos())

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if grid[row][col].celltype not in (CellType.START, CellType.END):
                    if not start:
                        grid[row][col].celltype = CellType.START
                        start = grid[row][col]
                    elif not end:
                        grid[row][col].celltype = CellType.END
                        end = grid[row][col]
                    else:
                        grid[row][col].celltype = CellType.BARRIER
                        is_drawing = True
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                if grid[row][col] == start:
                    start = None
                elif grid[row][col] == end:
                    end = None

                grid[row][col].celltype = CellType.NULL
        if event.type == pygame.MOUSEMOTION:
            if is_drawing:
                row, col = get_clicked_cell(pygame.mouse.get_pos())
                
                if grid[row][col].celltype not in (CellType.START, CellType.END):
                    grid[row][col].celltype = CellType.BARRIER
        if event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                is_started = True

                for row in grid:
                    for cell in row:
                        cell.find_neighbors(grid)

                calculate_shortest_path(lambda: draw(surface, grid), grid, start, end)
            if event.key == pygame.K_r:
                reset_grid()

    clock.tick(120)

pygame.quit()
sys.exit()

# TODO: 'win/surface' and 'grid' are global variables. Some functions get them as params others not. Choose one method.
