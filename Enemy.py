import pygame
import math
from Playerphysics import playerphysics
from Weapon import weapon


class enemy(playerphysics):
    def __init__(self, x, y, xsize, ysize, _speed, _accel, _deccel, _jump, _weapon="sandgun", xvel=0 , yvel=0, _airaccel=-1, _airdeccel=-1, _deugview=False):
        super().__init__(x, y, xvel, yvel, xsize, ysize, _speed, _accel, _deccel, _jump, _airaccel, _airdeccel, _deugview)

        self.availableguns = ["sandgun", "blockgun", "watergun"]
        self.gun = weapon(_weapon)
        self.dir = pygame.Vector2()

    def cycleweapons(self, direction):
        current = self.gun.weapontype
        i = self.availableguns.index(current)
        if direction > 0:
            if i < len(self.availableguns) - 1:
                i += 1
            else:
                i = 0
        else:
            if i != 0:
                i -= 1
            else:
                i = len(self.availableguns) - 1

        self.gun.weapontype = self.availableguns[i]

    def update(self, player, grid, gravity, dt, sandmanager):
        self.move = pygame.Vector2()
        dir = pygame.Vector2()

        self.dir = player.pos - self.pos
        if self.dir.length_squared() > 25:
            dir = self.dir

        self.updatephysics(dir, grid, gravity, dt)

        self.gun.updatebullets(dt, sandmanager, grid, gravity)

    def draw(self, screen):

        if self.debugview:
            br = self.pos + self.size / 2
            tl = self.pos - self.size / 2

            for i in range(1, math.floor(br.x + 1) - math.floor(tl.x) - 1):
                p1 = pygame.Rect(
                    math.floor(tl.x + i) * 16, math.floor(tl.y) * 16,
                    16, 16
                )  # translating from world to screen space

                p2 = pygame.Rect(
                    math.floor(tl.x + i) * 16, math.floor(br.y) * 16,
                    16, 16
                )  # translating from world to screen space

                pygame.draw.rect(screen, "green", p1)
                pygame.draw.rect(screen, "green", p2)

            for i in range(1, math.floor(br.y + 1) - math.floor(tl.y) - 1):
                p1 = pygame.Rect(
                    math.floor(tl.x) * 16, math.floor(tl.y + i) * 16,
                    16, 16
                )  # translating from world to screen space

                p2 = pygame.Rect(
                    math.floor(br.x) * 16, math.floor(tl.y + i) * 16,
                    16, 16
                )  # translating from world to screen space

                pygame.draw.rect(screen, "green", p1)
                pygame.draw.rect(screen, "green", p2)

            if self.colliding:
                colour = "red"
            else:
                colour = "blue"
        else:
            colour = "darkred"

        p = pygame.Rect(
            self.pos.x * 16 - self.size.x * 8, self.pos.y * 16 - self.size.y * 8,
            self.size.x * 16, self.size.y * 16
        )  # translating from world to screen space

        pygame.draw.rect(screen, colour, p)

        self.gun.draw(screen, self.pos, self.size, self.dir)