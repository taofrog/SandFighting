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
            else:
                tiles[x][y] = 0

tiles[10][10] = 1

p1 = Player.player(32, 32, 0, 0, 0.8, 0.8, 0.1, 0.99)
while run:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    dir = pygame.Vector2()
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

    p1.update(dir, tiles, pygame.Vector2())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

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
