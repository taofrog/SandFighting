import pygame
import math

# speed, colour gravity
bullets = {"sandgun"  : [32, "red"],
            "blockgun": [64, [80, 80, 80, 255]],
            "watergun": [32, "blue"]}

class projectile:
    def __init__(self, _pos, weapon, endpoint):
        self.pos = _pos
        self.weapontype = weapon
        self.endpoint = endpoint
        self.vel = endpoint - _pos
        self.vel = self.vel.normalize() * bullets[weapon][0]

    def tilecollision(self, grid):
        gridpos = self.pos
        surrounds = [grid[math.floor(gridpos.x / 16) - 1][math.floor(gridpos.y / 16)],
                     grid[math.floor(gridpos.x / 16) + 1][math.floor(gridpos.y / 16)],
                     grid[math.floor(gridpos.x / 16)][math.floor(gridpos.y / 16) - 1],
                     grid[math.floor(gridpos.x / 16)][math.floor(gridpos.y / 16) + 1]]

        for square in surrounds:
            if square != 0 and square != 3:
                return True

        return False

    def update(self, dt):
        self.pos += self.vel * dt * 16

        distance = self.pos - self.endpoint
        velscreen = self.vel * dt * 16

        if distance.length() <= velscreen.length():
            self.pos = self.endpoint
            return True

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, bullets[self.weapontype][1], self.pos, 10)
