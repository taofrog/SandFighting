import pygame
import math

import Enemy
import Player
from sandManager import *
from waveManager import wavemanager
from UIManager import UIManager

pygame.init()
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
run = True

gravity = pygame.Vector2(0.0, 0.6)

p1 = Player.player(32, 10, 2.5, 2.5, 16, 0.05, 0.01, 70, "blockgun", _deugview=False)
enemywaves = wavemanager()
# xpos, ypos, xvel, yvel, xsize, xsize, speed, accel, deccel, jump
# can also set custom airaccel and airdeccel, as well as toggle debug view

solid = tile(-1, [255, 255, 255, 255])
air = tile(0, [0, 0, 0, 0])
air.displacingTiles = []
sand = tile(1, [255, 0, 0, 255])
sand.gravity = True
sand.sandPhysics = True
block = tile(2, [80, 80, 80, 255])
block.gravity = True
water = tile(3, [0, 0, 255, 255])
water.gravity = True
water.sandPhysics = True
water.liquid = True
water.gravity = True
water.displacingTiles = [0]
boom = tile(4, [250, 200, 120, 255])
boom.temp = True

tileTypes = {
    -1:solid,
    0: air,
    1: sand,
    2: block,
    3: water,
    4: boom
}

manager = tileManager((64, 64), tileTypes)
for y in range(-1, 65):
    for x in range(-1, 65):
        if x == -1 or y == -1:
            manager.tiles[x][y] = -1
        elif x == 65 or y == 65:
            manager.tiles[x][y] = -1
        elif y > 32:
            manager.tiles[x][y] = 1

enemywaves.spawnenemy(manager.tiles, p1)
uimanager = UIManager(pygame.font.SysFont("Arial", 15))
titleManager = UIManager(pygame.font.SysFont("Arial", 50))

while run:
    dt = clock.tick(60)
    dt *= 0.001

    mousepos = pygame.mouse.get_pos()
    mousedown = False
    mousedown2 = False

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

            if event.key == pygame.K_e:
                gravity.x += 0.1
            if event.key == pygame.K_q:
                gravity.x -= 0.1
            if event.key == pygame.K_r:
                gravity.y -= 0.1
            if event.key == pygame.K_f:
                gravity.y += 0.1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('w'):
                dir.y += 1
            if event.key == pygame.K_RIGHT or event.key == ord('s'):
                dir.y -= 1
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                dir.x += 1
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                dir.x -= 1

        if event.type == pygame.MOUSEWHEEL:
            p1.cycleweapons(event.y)

    if pygame.mouse.get_pressed(3)[0]:
        mousedown = True
    if pygame.mouse.get_pressed(3)[2]:
        mousedown2 = True

    manager.update()
    enemywaves.update(manager.tiles, p1)

    # update player. takes directional input, 64x64 grid, and gravity
    substeps = 8
    for _ in range(substeps):
        dead = p1.update(dir, manager.tiles, gravity, dt / substeps, mousepos, mousedown, mousedown2, manager, enemywaves.enemies)
        enemywaves.updateenemies(p1, manager, gravity, dt / substeps)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # draw a rect for every solid cell
    if not dead:

        screen.blit(manager.displaySurf, [0, 0])
        manager.updateSurf(0, 0)

        p1.draw(screen)
        enemywaves.drawenemies(screen)

        uimanager.updateUIElement(screen, [10, 10], str(p1.health))

        for eneme in enemywaves.enemies:
            uimanager.updateUIElement(screen, [eneme.pos.x * 16, (eneme.pos.y - 3) * 16], str(eneme.health))
    else:
        titleManager.updateUIElement(screen, [400, 400], f"You Died! Score: {enemywaves.totalkills}")
        titleManager.updateUIElement(screen, [400, 450], f"Wave: {enemywaves.wave}")
    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()