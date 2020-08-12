import sys

import pygame

from colors import GREY, WHITE
from constants import CellType, HEIGHT, WIDTH, SIZE
from spot import Spot


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("A* Pathfinding Algorithm")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

def reset():
    # Reset points dictionary
    # Reset all cell to CellType.NULL
    pass

points = {
    CellType.START: None,
    CellType.END: None
}
grid = prepare_cell_data()
started = False
draw_line = False

while True:
    screen.fill(WHITE)
    draw_cells(screen, grid)
    draw_gridlines(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if started:
            continue
        if event.type == pygame.K_r:
            reset()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            row, col = get_clicked_cell(m_pos)

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if grid[row][col].celltype not in (CellType.START, CellType.END):
                    if not points[CellType.START]:
                        celltype = CellType.START
                    elif not points[CellType.END]:
                        celltype = CellType.END
                    else:
                        celltype = CellType.BARRIER
                        draw_line = True

                    points[celltype] = row, col
                    grid[row][col].celltype = celltype
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                celltype = grid[row][col].celltype

                points[celltype] = None
                grid[row][col].celltype = CellType.NULL
        if event.type == pygame.MOUSEMOTION:
            if draw_line:
                m_pos = pygame.mouse.get_pos()
                row, col = get_clicked_cell(m_pos)
                
                if grid[row][col].celltype not in (CellType.START, CellType.END):
                    grid[row][col].celltype = CellType.BARRIER
        if event.type == pygame.MOUSEBUTTONUP:
            draw_line = False

    clock.tick(120)
    pygame.display.update()
