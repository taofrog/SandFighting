import pygame
import math
from Playerphysics import playerphysics
from Weapon import weapon


class player(playerphysics):
    def __init__(self, x, y, xsize, ysize, _speed, _accel, _deccel, _jump, _weapon="sandgun", xvel=0 , yvel=0, _airaccel=-1, _airdeccel=-1, _deugview=False):
        super().__init__(x, y, xvel, yvel, xsize, ysize, _speed, _accel, _deccel, _jump, _airaccel, _airdeccel, _deugview)

        self.mouse = pygame.Vector2()
        self.availableguns = ["sandgun", "blockgun", "watergun", "grenade"]
        self.gun = weapon(_weapon)
        self.surfSheet = pygame.image.load("PinkGuyNoMouth.png")
        self.frame = 0
        self.mouthAnimateFrame = 0
        self.xSize = xsize * 16
        self.ySize = ysize * 16

        self.scaleDif = self.ySize / 32
        print(self.scaleDif)
        self.frames = []
        for frameI in range(3):
            subFrame = pygame.rect.Rect([0, 32 * frameI], [32, 32])
            frame = self.surfSheet.subsurface(subFrame)
            frame = pygame.transform.scale_by(frame, self.scaleDif)
            self.frames.append(frame)
        self.animateFrame = 0

        self.mouthSheet = pygame.image.load("Mouth.png")

        self.mouthFrame = 0
        self.mouthFrames = []
        for frameI in [0, 1]:
            subFrame = pygame.rect.Rect([0, 8 * frameI], [17, 8])
            frame = self.mouthSheet.subsurface(subFrame)
            frame = pygame.transform.scale_by(frame, self.scaleDif)
            self.mouthFrames.append(frame)


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

    def update(self, movement: pygame.Vector2, grid, gravity, dt, mousepos, mousedown, sandmanager):
        self.updatephysics(movement, grid, gravity, dt)

        self.mouse = mousepos

        if mousedown:
            self.gun.shoot(self.pos, self.size, mousepos)

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
            colour = "green"

        p = pygame.Rect(
            self.pos.x * 16 - self.size.x * 8, self.pos.y * 16 - self.size.y * 8,
            self.size.x * 16, self.size.y * 16
        )  # translating from world to screen space

        self.frame += 1
        self.mouthFrame += 1
        if self.mouthFrame % 10 == 0:
            self.mouthAnimateFrame += 1
        if self.mouthAnimateFrame > 1:
            self.mouthAnimateFrame = 0
        if self.frame % 10 == 0:
            self.animateFrame += 1
        if self.animateFrame > 2:
            self.animateFrame = 0



        screen.blit(self.frames[self.animateFrame], p)

        mouthOffset = pygame.Vector2((-8.5 * self.scaleDif) + (self.vel.x / 4), 0)



        screen.blit(self.mouthFrames[self.mouthAnimateFrame], p.center + mouthOffset)


        self.gun.draw(screen, self.pos, self.size, self.mouse)
