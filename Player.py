import pygame
import math

class player:
    def __init__(self, x, y, xvel, yvel, xsize, ysize, _speed, _damp, _jump, _airspeed=-1, _airdamp=-1):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(xvel, yvel)
        self.move = pygame.Vector2()
        self.size = pygame.Vector2(xsize, ysize)
        self.speed = _speed
        self.damp = _damp
        self.jump = _jump
        self.colliding = False
        self.grounded = False
        self.jtime = 0.1
        if _airspeed < 0:
            self.airspeed = self.speed/10
        else:
            self.airspeed = _airspeed
        if _airspeed < 0:
            self.airdamp = math.log10(self.damp) / 3 + 1
        else:
            self.airdamp = _airdamp

    def tilecollisions(self, grid, gravity):
        overlap = pygame.Vector2()  # initialising empty variable

        gridpos = [math.floor(self.pos.x), math.floor(self.pos.y)]  # what cell the player is currently in. int for ease

        # check if center is inside a block i think it will squish here. need to look out for bugs
        if grid[gridpos[0]][gridpos[1]] == 1:
            self.colliding = True
            return
        else:
            self.colliding = False

        # check if each surrounding cell is solid, and check if there is any overlap with that cell.

        leftsquares = []
        rightsquares = []
        topsquares = []
        bottomsquares = []

        br = self.pos + self.size / 2
        tl = self.pos - self.size / 2
        bl = pygame.Vector2(br.x, tl.y)
        tr = pygame.Vector2(tl.x, br.y)

        for cornerpos in [tl, tr, bl, br]:
            if grid[int(cornerpos.x)][int(cornerpos.y)] == 1:
                self.colliding = True

                if cornerpos.x < self.pos.x:
                    xoverlap = cornerpos.x - math.floor(cornerpos.x) - 1
                else:
                    xoverlap = cornerpos.x - math.floor(cornerpos.x)

                if cornerpos.y < self.pos.y:
                    yoverlap = cornerpos.y - math.floor(cornerpos.y) - 1
                else:
                    yoverlap = cornerpos.y - math.floor(cornerpos.y)

                if abs(xoverlap) > abs(yoverlap):
                    overlap.y = yoverlap
                else:
                    overlap.x = xoverlap

        if overlap.y == 0:
            for i in range(1, math.floor(br.x + 1) - math.floor(tl.x) - 1):
                topsquares.append(pygame.Vector2(math.floor(tl.x + i), math.floor(tl.y)))
                bottomsquares.append(pygame.Vector2(math.floor(tl.x + i), math.floor(br.y)))

        if overlap.x == 0:
            for i in range(1, math.floor(br.y + 1) - math.floor(tl.y) - 1):
                leftsquares.append(pygame.Vector2(math.floor(tl.x), math.floor(tl.y + i)))
                rightsquares.append(pygame.Vector2(math.floor(br.x), math.floor(tl.y + i)))

        for square in topsquares:
            if grid[int(square.x)][int(square.y)] == 1:
                self.colliding = True
                overlap.y = self.pos.y - self.size.y / 2 - (square.y + 1)
                break

        for square in bottomsquares:
            if grid[int(square.x)][int(square.y)] == 1:
                self.colliding = True
                overlap.y = self.pos.y + self.size.y / 2 - square.y
                break

        for square in leftsquares:
            if grid[int(square.x)][int(square.y)] == 1:
                self.colliding = True
                overlap.x = self.pos.x - self.size.x / 2 - (square.x + 1)
                break

        for square in rightsquares:
            if grid[int(square.x)][int(square.y)] == 1:
                self.colliding = True
                overlap.x = self.pos.x + self.size.x / 2 - square.x
                break

        # send position to outside cells
        self.pos -= overlap

        if overlap.y * gravity.y > 0 or overlap.x * gravity.x > 0:
            self.grounded = True
        else:
            self.grounded = False

        # set velocity of the colliding axis to 0 if there is significant overlap
        if abs(overlap.x) > self.size.x / 50:
            self.vel.x = 0
        if abs(overlap.y) > self.size.x / 50:
            self.vel.y = 0

    def update(self, movement, grid, gravity, dt):
        # MOVEMENT
        # make jump height consistant for dif damp and speed factors since its done weirdly
        # doesnt quite work, changing speed slightly changes jump height. damp doesnt tho
        # this works for any axis aligned gravity. non axis aligned is broken but the controls are also broken
        """jumpscale = self.jump / (self.speed * self.damp)
        jumpmod = pygame.Vector2((abs(gravity.x * jumpscale) + 1), (abs(gravity.y * jumpscale) + 1))
        movement = movement.elementwise() * jumpmod
        self.move += movement

        if self.grounded:
            self.vel += self.speed * self.move / 60
            self.vel *= self.damp
        else:
            self.vel += self.airspeed * self.move / 60
            self.vel *= self.airdamp"""

        self.move += movement

        gravangle = math.atan2(gravity.x, gravity.y)
        gravspacevel = self.vel.rotate_rad(gravangle)
        gravspacemove = self.move.rotate_rad(gravangle)

        if self.grounded:
            gravspacevel.x += self.speed * gravspacemove.x
            gravspacevel.x *= self.damp
            if gravspacemove.y < 0:
                gravspacevel.y -= self.jump
        else:
            gravspacevel.x += self.airspeed * gravspacemove.x
            gravspacevel.x *= self.airdamp

        self.vel = gravspacevel.rotate_rad(-gravangle)

        self.vel += gravity  # idk where to put this. shouldnt change much though

        self.pos += self.vel * dt  # move by vel each frame

        # COLLISIONS
        self.tilecollisions(grid, gravity)  # check for collisions with the grid.
        # any other collisions, eg projectiles, should go here

    def draw(self, screen):
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

        p = pygame.Rect(
            self.pos.x * 16 - self.size.x * 8, self.pos.y * 16 - self.size.y * 8,
            self.size.x * 16, self.size.y * 16
        )  # translating from world to screen space

        if self.colliding:
            colour = "red"
        else:
            colour = "blue"

        pygame.draw.rect(screen, colour, p)


