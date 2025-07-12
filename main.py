import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption("Sand-Simulator")

CELL_SIZE = 4
GRID_WIDTH = screen.get_width() // CELL_SIZE
GRID_HEIGHT = screen.get_height() // CELL_SIZE

grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

last_placed_time = 0
placement_delay = 50  # milliseconds

last_updated_time = 0
update_delay = 40

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0, 0, 0))

    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - last_placed_time > placement_delay:
        pos = pygame.mouse.get_pos()
        gx = pos[0] // CELL_SIZE
        gy = pos[1] // CELL_SIZE

        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            grid[gy][gx] = (255, 255, 0)
            last_placed_time = pygame.time.get_ticks()

    if pygame.time.get_ticks() - last_updated_time > update_delay:
        for y in range(GRID_HEIGHT - 2, -1, -1):
            for x in range(GRID_WIDTH):
                if grid[y][x] and grid[y+1][x] is None:
                    grid[y+1][x] = grid[y][x]
                    grid[y][x] = None
                elif grid[y][x] and grid[y+1][x] is not None:
                    direction = random.choice([-1, 1])
                    if 0 <= x + direction < GRID_WIDTH and grid[y+1][x+direction] is None:
                        grid[y+1][x+direction] = grid[y][x]
                        grid[y][x] = None

        last_updated_time = pygame.time.get_ticks()


    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()