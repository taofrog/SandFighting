import pygame
import math

class player:
    def __init__(self, x, y, xvel, yvel, xsize, ysize, _speed, _damp):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(xvel, yvel)
        self.move = pygame.Vector2()
        self.size = pygame.Vector2(xsize, ysize)
        self.speed = _speed
        self.damp = _damp
        self.colliding = False

    def tilecollisions(self, grid):
        overlap = pygame.Vector2()

        gridpos = [math.floor(self.pos.x), math.floor(self.pos.y)]
        if grid[gridpos[0]][gridpos[1]] == 1:
            self.colliding = True
        else:
            self.colliding = False

        if grid[gridpos[0] + 1][gridpos[1]] == 1:  # left
            if self.pos.x + self.size.x / 2 >= gridpos[0] + 1:
                self.colliding = True
                overlap.x = self.pos.x + self.size.x / 2 - (gridpos[0] + 1)

        if grid[gridpos[0] - 1][gridpos[1]] == 1:  # right
            if self.pos.x - self.size.x / 2 <= gridpos[0]:
                self.colliding = True
                overlap.x = self.pos.x - self.size.x / 2 - gridpos[0]

        if grid[gridpos[0]][gridpos[1] + 1] == 1:  # below
            if self.pos.y + self.size.y / 2 >= gridpos[1] + 1:
                self.colliding = True
                overlap.y = self.pos.y + self.size.y / 2 - (gridpos[1] + 1)

        if grid[gridpos[0]][gridpos[1] - 1] == 1:  # above
            if self.pos.y - self.size.y / 2 <= gridpos[1]:
                self.colliding = True
                overlap.y = self.pos.y - self.size.y / 2 - gridpos[1]

        if grid[gridpos[0] + 1][gridpos[1] + 1] == 1:  # bottom right
            if self.pos.x + self.size.x / 2 >= gridpos[0] + 1 and self.pos.y + self.size.y / 2 >= gridpos[1] + 1:
                self.colliding = True
                overlapx = self.pos.x + self.size.x / 2 - (gridpos[0] + 1)
                overlapy = self.pos.y + self.size.y / 2 - (gridpos[1] + 1)
                if abs(overlapx) > abs(overlapy):
                    overlap.y = overlapy
                else:
                    overlap.x = overlapx

        if grid[gridpos[0] + 1][gridpos[1] - 1] == 1:  # top right
            if self.pos.x + self.size.x / 2 >= gridpos[0] + 1 and self.pos.y - self.size.y / 2 <= gridpos[1]:
                self.colliding = True
                overlapx = self.pos.x + self.size.x / 2 - (gridpos[0] + 1)
                overlapy = self.pos.y - self.size.y / 2 - gridpos[1]
                if abs(overlapx) > abs(overlapy):
                    overlap.y = overlapy
                else:
                    overlap.x = overlapx

        if grid[gridpos[0] - 1][gridpos[1] + 1] == 1:  # bottom left
            if self.pos.x - self.size.x / 2 <= gridpos[0] and self.pos.y + self.size.y / 2 >= gridpos[1] + 1:
                self.colliding = True
                overlapx = self.pos.x - self.size.x / 2 - gridpos[0]
                overlapy = self.pos.y + self.size.y / 2 - (gridpos[1] + 1)
                if abs(overlapx) > abs(overlapy):
                    overlap.y = overlapy
                else:
                    overlap.x = overlapx

        if grid[gridpos[0] - 1][gridpos[1] - 1] == 1:  # top left
            if self.pos.x - self.size.x / 2 <= gridpos[0] and self.pos.y - self.size.y / 2 <= gridpos[1]:
                self.colliding = True
                overlapx = self.pos.x - self.size.x / 2 - gridpos[0]
                overlapy = self.pos.y - self.size.y / 2 - gridpos[1]
                if abs(overlapx) > abs(overlapy):
                    overlap.y = overlapy
                else:
                    overlap.x = overlapx

        self.pos -= overlap
        if abs(overlap.x) > self.size.x / 50:
            self.vel.x = 0
        if abs(overlap.y) > self.size.x / 50:
            self.vel.y = 0

    def update(self, movement, grid, gravity):
        # MOVEMENT
        self.move += movement

        self.vel += self.speed * self.move / 60
        self.vel *= self.damp
        self.vel += gravity

        self.pos += self.vel

        # COLLISIONS
        self.tilecollisions(grid)


    def draw(self, screen):
        p = pygame.Rect(
            self.pos.x * 16 - self.size.x * 8, self.pos.y * 16 - self.size.y * 8,
            self.size.x * 16, self.size.y * 16
        )
        if self.colliding:
            colour = "red"
        else:
            colour = "blue"
        pygame.draw.rect(screen, colour, p)
