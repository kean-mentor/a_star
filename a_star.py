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
    cols = WIDTH // SIZE
    rows = HEIGHT // SIZE
 
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            spot = Spot(c, r, rows)
            grid[r].append(spot)

    return grid


def draw_cells(win, grid):
    for row in grid:
        for spot in row:
            spot.draw(win)

def draw_gridlines(win):
    cols = WIDTH // SIZE
    rows = HEIGHT // SIZE

    for r in range(rows):
        pygame.draw.line(win, GREY, (0, r * SIZE), (WIDTH, r * SIZE))

    for c in range(cols):
        pygame.draw.line(win, GREY, (c * SIZE, 0), (c * SIZE, HEIGHT))


def get_clicked_cell(m_pos):
    row = m_pos[1] // SIZE
    col = m_pos[0] // SIZE

    return row, col


def reset_grid():
    # FYI: Think about global variables :(
    points[CellType.START] = None
    points[CellType.END] = None

    for row in grid:
        for cell in row:
            cell.celltype = CellType.NULL


grid = prepare_cell_data()
points = {CellType.START: None, CellType.END: None}  # Important cell locations
is_started = False  # Pathfinding algorithm started or not
is_drawing = False  # Start and end points placed and left mouse button is pressed
is_running = True


while is_running:
    surface.fill(WHITE)
    draw_cells(surface, grid)
    draw_gridlines(surface)

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
                    if not points[CellType.START]:
                        celltype = CellType.START
                    elif not points[CellType.END]:
                        celltype = CellType.END
                    else:
                        celltype = CellType.BARRIER
                        is_drawing = True

                    points[celltype] = row, col
                    grid[row][col].celltype = celltype  # FIXME: Barrier is also added but it is unnecessary
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                celltype = grid[row][col].celltype

                points[celltype] = None
                grid[row][col].celltype = CellType.NULL
        if event.type == pygame.MOUSEMOTION:
            if is_drawing:
                row, col = get_clicked_cell(pygame.mouse.get_pos())
                
                if grid[row][col].celltype not in (CellType.START, CellType.END):
                    grid[row][col].celltype = CellType.BARRIER
        if event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            if event.key == pygame.K_r:
                reset_grid()

    clock.tick(120)
    pygame.display.update()

pygame.quit()
sys.exit()
