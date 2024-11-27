
import pygame
import math
from Playerphysics import playerphysics
from Weapon import weapon
pygame.mixer.init()


class enemy(playerphysics):
    def __init__(self, x, y, xsize, ysize, _speed, _accel, _deccel, _jump, _weapon="sandgun", xvel=0 , yvel=0, _airaccel=-1, _airdeccel=-1, _deugview=False):
        super().__init__(x, y, xvel, yvel, xsize, ysize, _speed, _accel, _deccel, _jump, _airaccel, _airdeccel, _deugview)

        self.availableguns = ["sandgun", "blockgun", "watergun"]
        self.gun = weapon(_weapon)
        self.dir = pygame.Vector2()
        self.cooldown = 0
        self.ySize = ysize * 16

        self.hitdelay = 0.8

        self.damage = 4

        self.triestobreak = 500
        self.boredOfX = 0
        self.lastCoords = pygame.Vector2(self.pos.x, self.pos.y)
        self.frame = 0
        self.spriteSheet = pygame.image.load("Assets/RedBoiiiiii.png")
        self.hurtSFX = pygame.mixer.Sound("SFX/hitHurt.wav")
        self.hurtSFX.set_volume(0.3)

        self.scaleDif = self.ySize / 32
        self.frames = []
        for frameI in range(3):
            subFrame = pygame.rect.Rect([0, 32 * frameI], [32, 32])
            frame = self.spriteSheet.subsurface(subFrame)
            frame = pygame.transform.scale_by(frame, self.scaleDif)
            self.frames.append(frame)
        self.animateFrame = 0

        self.health = 100

    def dealdamage(self):
        if self.cooldown <= 0:
            self.cooldown = self.hitdelay
            return self.damage
        return 0

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
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= dt
        self.move = pygame.Vector2()
        dir = pygame.Vector2()

        self.dir = player.pos - self.pos
        if self.dir.length_squared() > 25:
            dir = self.dir

        if abs(self.lastCoords.x - self.pos.x) <= 0.01:
            self.boredOfX += 1
        else:
            self.boredOfX = 0
        tilePos = [int(self.pos.x), int(self.pos.y)]

        if self.boredOfX >= self.triestobreak:
            facing = math.copysign(1, dir.x) * 2

            sandmanager.tiles[int(tilePos[0] + facing)][tilePos[1]] = 0
            #sandmanager.tiles[tilePos[0]][3] = 2

        self.lastCoords = pygame.Vector2(self.pos.x, self.pos.y)

        self.gun.updatebullets(dt, sandmanager, grid, gravity)

        selfrect = pygame.Rect(self.pos - (self.size / 2), self.size)

        worlddamage = self.updatephysics(dir, grid, gravity, dt)
        bulletstouching = player.gun.checkcollision(selfrect)
        bullets2touching = player.gun2.checkcollision(selfrect)
        playerdamage = len(bulletstouching)
        totalDamage = worlddamage + playerdamage
        self.health -= totalDamage
        if totalDamage > 0:
            self.hurtSFX.play()

        if self.health <= 0:
            return True

        return False

    def draw(self, screen, screensize, offsetx, offsety):
        minscreen = min(screensize[0], screensize[1])
        scale = minscreen / 64

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
            self.pos.x * scale - self.size.x * scale / 2 + offsetx, self.pos.y * scale - self.size.y * scale / 2 + offsety,
            self.size.x * scale, self.size.y * scale
        )  # translating from world to screen space

        self.frame += 1

        if self.frame % 10 == 0:
            self.animateFrame += 1
        if self.animateFrame > 2:
            self.animateFrame = 0

        frame = pygame.transform.scale_by(self.frames[self.animateFrame], scale / 16)

        if self.health > 0:
            screen.blit(frame, p)
