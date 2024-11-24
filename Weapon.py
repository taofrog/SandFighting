import pygame
import math
from Bullet import projectile

weaponcolours = {"sandgun": "red",}
weaponreloadtimes = {"sandgun": 0.1}

class weapon:
    def __init__(self, _type):
        self.weapontype = _type
        self.bullets = []
        self.reload = 0

    def updatebullets(self, dt, sandmanager):
        if self.reload > 0:
            self.reload -= dt
        else:
            self.reload = 0

        for bullet in self.bullets:
            if bullet.update(dt):
                if self.weapontype == "sandgun":
                    self.bullets.remove(bullet)
                    sandmanager.tiles[math.floor(bullet.pos.x/16)][math.floor(bullet.pos.y/16)] = 1

    def shoot(self, pos, size, mousepos):
        if self.reload == 0:
            mousedir = mousepos - pos * 16
            mousedir = mousedir.normalize()

            gunpos = pos * 16 - size * 2 + (mousedir.elementwise() * size) * 8

            self.bullets.append(projectile(gunpos, self.weapontype, mousepos))

            self.reload = weaponreloadtimes[self.weapontype]

    def draw(self, screen, pos, size, mousepos):
        mousedir = mousepos - pos * 16
        mousedir = mousedir.normalize()

        gunpos = pos * 16 - size * 2 + (mousedir.elementwise() * size) * 8

        if self.weapontype == "sandgun":
            g = pygame.Rect(
                gunpos.x, gunpos.y,
                size.x * 4, size.y * 4
            )  # translating from 0world to screen space

            pygame.draw.rect(screen, weaponcolours["sandgun"], g)

        for bullet in self.bullets:
            bullet.draw(screen)
