import pygame
import math

bulletspeeds = {"sandgun" : 32,
                "blockgun": 64}
bulletcolours = {"sandgun" : "red",
                 "blockgun": [80, 80, 80, 255]}

class projectile:
    def __init__(self, _pos, weapon, endpoint):
        self.pos = _pos
        self.weapontype = weapon
        self.endpoint = endpoint
        self.vel = endpoint - _pos
        self.vel = self.vel.normalize() * bulletspeeds[weapon]

    def update(self, dt):
        self.pos += self.vel * dt * 16

        distance = self.pos - self.endpoint
        velscreen = self.vel * dt * 16

        if distance.length() <= velscreen.length():
            return True

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, bulletcolours[self.weapontype], self.pos, 10)
