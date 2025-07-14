import pygame
import random
from sand_texture_loader import *

pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((600, 600))

pygame.display.set_caption("Sand-Simulator")

CELL_SIZE = 4
GRID_WIDTH = screen.get_width() // CELL_SIZE
GRID_HEIGHT = screen.get_height() // CELL_SIZE

grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

last_placed_time = 0
placement_delay = 00  # milliseconds

last_updated_time = 0
update_delay = 40

gravity = 0.2

pygame.time.Clock()

sand_palette, sand_probs = load_palette_and_weights("sand")
gravel_palette, gravel_probs = load_palette_and_weights("gravel")

materials = {
    "sand": {"name": "Sand","palette": sand_palette, "prob": sand_probs},
    "gravel": {"name": "Gravel", "palette": gravel_palette, "prob": gravel_probs},
}
active_material = materials["sand"]
status_text = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #this is if player presses closes tab then the program quits
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                active_material = materials["sand"]
            elif event.key == pygame.K_2:
                active_material = materials["gravel"]
            elif event.key == pygame.K_c:
                grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            elif event.key == pygame.K_f:
                if update_delay != 40:
                    update_delay = 40
                    status_text = ""
                else:
                    update_delay = 200000000000
                    status_text = "Time: Frozen"


    screen.fill((0, 0, 0))  #fills screen with a black background

    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - last_placed_time > placement_delay:
        #checking if mouse left click is pressed and a delay timer so the clicks are not too fast
        pos = pygame.mouse.get_pos()
        gx = pos[0] // CELL_SIZE
        gy = pos[1] // CELL_SIZE

        if 0 <= gx < GRID_WIDTH  and 0 <= gy < GRID_HEIGHT:
            for y in range(-5,5):
                for x in range(-5,5):
                    if 0 <= gx+x < GRID_WIDTH and 0 <= gy+y < GRID_HEIGHT:
                        if grid[gy+y][gx+x] is None:
                            grid[gy+y][gx+x] = {"color" : random.choices(active_material["palette"], weights=active_material["prob"])[0], "vy" : 1.0}    #places active material with velocity 1(if velocity is less than 1 then block will not move
                            last_placed_time = pygame.time.get_ticks()      #updated timer

    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        gx = pos[0] // CELL_SIZE
        gy = pos[1] // CELL_SIZE

        if 0 <= gx < GRID_WIDTH  and 0 <= gy < GRID_HEIGHT:
            for y in range(-5,5):
                for x in range(-5,5):
                    if 0 <= gx+x < GRID_WIDTH and 0 <= gy+y < GRID_HEIGHT:
                        if grid[y+gy][x+gx]:
                            grid[y+gy][x+gx] = None


    if pygame.time.get_ticks() - last_updated_time > update_delay:
        for y in range(GRID_HEIGHT - 2, -1, -1):
            x_range = list(range(GRID_WIDTH))
            random.shuffle(x_range)

            for x in x_range:
                if grid[y][x]:
                    vy = grid[y][x]["vy"]
                    max_new_y = y + int(vy)

                    for new_y in range(max_new_y, y, -1):
                        if 0 <= new_y < GRID_HEIGHT and grid[new_y][x] is None:
                            grid[y][x]["vy"] += gravity
                            grid[new_y][x] = grid[y][x]
                            grid[y][x] = None
                            break

                    if grid[y][x] and grid[y+1][x]:
                        grid[y][x]['vy'] = 1.0      #Reset velocity when it is blocked
                        direction = random.choice([-1, 1])
                        if 0 <= x + direction < GRID_WIDTH and grid[y+1][x+direction] is None:
                            grid[y+1][x+direction] = grid[y][x]
                            grid[y][x] = None

        last_updated_time = pygame.time.get_ticks()


    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x]['color'],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    text = font.render("Material: " + active_material["name"], True, (255, 255, 255))
    screen.blit(text, (10, 10))
    status = font.render(status_text, True, (255, 255, 255))
    screen.blit(status, (10, 30))
    pygame.display.flip()