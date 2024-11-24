import pygame
import math

bulletspeeds = {"sandgun": 320,}
bulletcolours = {"sandgun": "red",}

class projectile:
    def __init__(self, _pos, weapon, endpoint):
        self.pos = _pos
        self.weapontype = weapon
        self.endpoint = endpoint
        self.vel = endpoint - _pos
        self.vel = self.vel.normalize() * bulletspeeds[weapon]

    def update(self, dt):
        self.pos += self.vel * dt

        distance = self.pos - self.endpoint
        velscreen = self.vel * dt

        if distance.length() <= velscreen.length():
            return True

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, bulletcolours["sandgun"], self.pos, 10)
