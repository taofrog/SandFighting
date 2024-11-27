import pygame
import math
from Bullet import projectile
pygame.mixer.init()
weaponcolours = {"sandgun" : "red",
                 "blockgun": [80, 80, 80, 255],
                 "watergun": "blue",
                 "grenade" : "darkgreen"}  # pygame colour literal
weaponreloadtimes = {"sandgun" : 0.08,
                     "blockgun": 0.12,
                     "watergun": 0.05,
                     "grenade" : 1} # time between bullets, in seconds\

weaponSoundsOnLand = {"sandgun" : pygame.mixer.Sound("SFX/sandWalk.wav"),
                     "blockgun": pygame.mixer.Sound("SFX/blockShoot.wav"),
                     "watergun": pygame.mixer.Sound("SFX/waterShoot.wav"),
                     "grenade" : pygame.mixer.Sound("SFX/explosion.wav")}
genericWeaponShoot = pygame.mixer.Sound("SFX/genericShoot.wav")
genericWeaponShoot.set_volume(0.05)
weaponSoundsOnLand["blockgun"].set_volume(0.05)
weaponSoundsOnLand["grenade"].set_volume(0.25)

class weapon:
    def __init__(self, _type):
        self.weapontype = _type
        self.bullets = []
        self.reload = 0

    def checkcollision(self, rect:pygame.Rect):
        touching = []
        for bullet in self.bullets:
            if rect.collidepoint(bullet.pos):
                touching.append(bullet.vel.length())
                bullet.endpoint = bullet.pos

        return touching

    def updatebullets(self, dt, sandmanager, grid, gravity):
        if self.reload > 0:
            self.reload -= dt
        else:
            self.reload = 0

        for bullet in self.bullets:
            if bullet.update(dt, gravity) or bullet.tilecollision(grid):

                if bullet.weapontype == "sandgun":
                    sandmanager.tiles[math.floor(bullet.pos[0])][math.floor(bullet.pos[1])] = 1
                if bullet.weapontype == "blockgun":
                    sandmanager.tiles[math.floor(bullet.pos[0])][math.floor(bullet.pos[1])] = 2
                if bullet.weapontype == "watergun":
                    for i in range(0, 1):
                        if 0 <= math.floor(bullet.pos[0]) + i <= 63:
                            sandmanager.tiles[math.floor(bullet.pos[0]) + i][math.floor(bullet.pos[1])] = 3
                if bullet.weapontype == "grenade":
                    explosionradius = 5

                    for x in range(-explosionradius, explosionradius + 1):
                        for y in range(-explosionradius, explosionradius + 1):
                            if 0 <= math.floor(bullet.pos[0])+x <= 63 \
                                    and 0 <= math.floor(bullet.pos[1])+y <= 63:
                                sandmanager.tiles[math.floor(bullet.pos[0])+x][math.floor(bullet.pos[1])+y] = 4
                weaponSoundsOnLand[bullet.weapontype].play()

                self.bullets.remove(bullet)

    def shoot(self, pos, size, mousepos):
        if self.reload == 0:
            mousedir = mousepos - pos
            mousedir = mousedir.normalize()

            gunpos = pos - size / 8 + (mousedir.elementwise() * size) / 2

            self.bullets.append(projectile(gunpos, self.weapontype, mousepos))

            self.reload = weaponreloadtimes[self.weapontype]
            genericWeaponShoot.play()

    def draw(self, screen, scale, offsetx, offsety, pos, size, mousepos):
        mousedir = mousepos - pos
        mousedir = mousedir.normalize()

        gunpos = (pos - size / 8 + (mousedir.elementwise() * size) / 2) * scale

        g = pygame.Rect(
            gunpos.x + offsetx, gunpos.y + offsety,
            size.x * scale / 4, size.y * scale / 4
        )  # translating from 0world to screen space

        pygame.draw.rect(screen, weaponcolours[self.weapontype], g)

        for bullet in self.bullets:
            bullet.draw(screen, scale, offsetx, offsety)
