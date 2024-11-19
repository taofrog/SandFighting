import pygame
import math
import Player
from sandManager import *

pygame.init()
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
run = True



gravity = pygame.Vector2(0.0, 0.6)

p1 = Player.player(32, 10, 0, 0, 2, 2, 0.2, 0.95, 50)

air = tile(0, [0, 0, 0, 0])
air.gravity = False
air.sandPhysics = False
sand = tile(1, [255, 0, 0, 255])

tileTypes = {
    0 : air,
    1 : sand
}

manager = tileManager((64, 64), tileTypes)
for y in range(31, 64):
    for x in range(0, 64):
        manager.tiles[x][y] = 1

# xpos, ypos, xvel, yvel, xsize, xsize, speed, dampening, jump

while run:
    dt = clock.tick(60)
    dt *= 0.001

    dir = pygame.Vector2()  # dir is a vector2 of each direction being pressed, to pass a single value to player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('w'):
                dir.y -= 1
            if event.key == pygame.K_RIGHT or event.key == ord('s'):
                dir.y += 1
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                dir.x -= 1
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                dir.x += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('w'):
                dir.y += 1
            if event.key == pygame.K_RIGHT or event.key == ord('s'):
                dir.y -= 1
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                dir.x += 1
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                dir.x -= 1
    if pygame.mouse.get_pressed(3)[0]:
        gridPos = pygame.mouse.get_pos()
        gridPos = [int(gridPos[0] / manager.scale), int(gridPos[1] / manager.scale)]
        manager.tiles[gridPos[0]][gridPos[1]] = 1



    manager.update()


    # update player. takes directional input, 64x64 grid, and gravity
    substeps = 8
    for _ in range(substeps):
        p1.update(dir, manager.tiles, gravity, dt / substeps)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    # draw a rect for every solid cell





    screen.blit(manager.displaySurf, [0, 0])
    manager.updateSurf(0, 0)

    p1.draw(screen)


    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
