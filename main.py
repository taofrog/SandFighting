import pygame
import math
import Player

pygame.init()
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
run = True

tiles = [[0 for y in range(64)] for y in range(64)]
for y in range(64):
    for x in range(64):
        if y * 64 + x > 2100:
            if (x + y % 2) % 2:
                print(x)
                tiles[x][y] = 1
        if y == 0 or x == 0:
            tiles[x][y] = 1
        if y == 63 or x == 63:
            tiles[x][y] = 1
        if y == 30 and x > 27 and x < 37:
            tiles[x][y] = 1

tiles[10][10] = 1

p1 = Player.player(32, 10, 0, 0, 5, 5, 2, 0.8, 20)
# xpos, ypos, xvel, yvel, xsize, xsize, speed, dampening, jump

while run:

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


    # update player. takes directional input, 64x64 grid, and gravity(broken)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    p1.update(dir, tiles, pygame.Vector2(0.0, 0.01))
    # draw a rect for every solid cell
    for y in range(64):
        for x in range(64):
            if tiles[x][y] == 1:
                r = pygame.Rect(x * 16, y * 16, 16, 16)
                pygame.draw.rect(screen, "black", r)

    p1.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
