import pygame
import math
from Bullet import projectile

weaponcolours = {"sandgun" : "red",
                 "blockgun": [80, 80, 80, 255],
                 "watergun": "blue"}  # pygame colour literal
weaponreloadtimes = {"sandgun" : 0.1,
                     "blockgun": 0.1,
                     "watergun": 0.1} # time between bullets, in seconds

class weapon:
    def __init__(self, _type):
        self.weapontype = _type
        self.bullets = []
        self.reload = 0

    def updatebullets(self, dt, sandmanager, grid):
        if self.reload > 0:
            self.reload -= dt
        else:
            self.reload = 0

        for bullet in self.bullets:
            if bullet.update(dt) or bullet.tilecollision(grid):
                if bullet.weapontype == "sandgun":
                    sandmanager.tiles[math.floor(bullet.pos[0] / 16)][math.floor(bullet.pos[1] / 16)] = 1
                if bullet.weapontype == "blockgun":
                    sandmanager.tiles[math.floor(bullet.pos[0] / 16)][math.floor(bullet.pos[1] / 16)] = 2
                if bullet.weapontype == "watergun":
                    sandmanager.tiles[math.floor(bullet.pos[0] / 16)][math.floor(bullet.pos[1] / 16)] = 3
                    sandmanager.tiles[math.floor(bullet.pos[0] / 16) + 1][math.floor(bullet.pos[1] / 16)] = 3
                    sandmanager.tiles[math.floor(bullet.pos[0] / 16) - 1][math.floor(bullet.pos[1] / 16)] = 3

                self.bullets.remove(bullet)

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

        g = pygame.Rect(
            gunpos.x, gunpos.y,
            size.x * 4, size.y * 4
        )  # translating from 0world to screen space

        pygame.draw.rect(screen, weaponcolours[self.weapontype], g)

        for bullet in self.bullets:
            bullet.draw(screen)
