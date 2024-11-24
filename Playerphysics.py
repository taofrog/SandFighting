import pygame
import math


class playerphysics:
    def __init__(self, x, y, xvel, yvel, xsize, ysize, _speed, _accel, _deccel, _jump, _airaccel, _airdeccel, _deugview):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(xvel, yvel)
        self.move = pygame.Vector2()
        self.size = pygame.Vector2(xsize, ysize)
        self.speed = _speed
        self.accel = _accel
        self.deccel = _deccel
        self.jump = _jump
        self.colliding = False
        self.grounded = False
        self.jtime = 0.1
        if _airaccel < 0:
            self.airaccel = self.accel / 5
        else:
            self.airaccel = _airaccel
        if _airdeccel < 0:
            self.airdeccel = self.deccel / 5
        else:
            self.airdeccel = _airdeccel

        self.debugview = _deugview

        self.stopthingsbreaking = 0.0001

    def axistilecollisions(self, grid, axis, gravity):
        overlap = 0  # initialising empty variable

        gridpos = [int(self.pos.x), int(self.pos.y)]

        br = self.pos + self.size / 2
        tl = self.pos - self.size / 2
        bl = pygame.Vector2(br.x, tl.y)
        tr = pygame.Vector2(tl.x, br.y)

        corner = False

        if axis == 0:
            leftsquares = []
            rightsquares = []

            for cornerpos in [tl, tr, bl, br]:
                if grid[int(cornerpos.x)][int(cornerpos.y)] != 0:
                    self.colliding = True

                    if cornerpos.x < self.pos.x:
                        overlap = cornerpos.x - math.floor(cornerpos.x) - 1
                    else:
                        overlap = cornerpos.x - math.floor(cornerpos.x)

                    if (cornerpos.y - self.pos.y) * gravity.y > 0:
                        corner = True

            #if overlap == 0:
            for i in range(1, math.floor(br.y + 1) - math.floor(tl.y) - 1):
                leftsquares.append(pygame.Vector2(math.floor(tl.x), math.floor(tl.y + i)))
                rightsquares.append(pygame.Vector2(math.floor(br.x), math.floor(tl.y + i)))

            for square in leftsquares:
                if grid[int(square.x)][int(square.y)] != 0:
                    self.colliding = True
                    overlap = self.pos.x - self.size.x / 2 - (square.x + 1)

                    corner = False
                    break

            for square in rightsquares:
                if grid[int(square.x)][int(square.y)] != 0:
                    self.colliding = True
                    overlap = self.pos.x + self.size.x / 2 - square.x

                    corner = False
                    break

        elif axis == 1:
            topsquares = []
            bottomsquares = []

            for cornerpos in [tl, bl, tr, br]:
                if grid[int(cornerpos.x)][int(cornerpos.y)] != 0:
                    self.colliding = True

                    if cornerpos.y < self.pos.y:
                        overlap = cornerpos.y - math.floor(cornerpos.y) - 1
                    else:
                        overlap = cornerpos.y - math.floor(cornerpos.y)

                    if (cornerpos.x - self.pos.x) * gravity.x > 0:
                        corner = True

            if overlap == 0:
                for i in range(1, math.floor(br.x + 1) - math.floor(tl.x) - 1):
                    topsquares.append(pygame.Vector2(math.floor(tl.x + i), math.floor(tl.y)))
                    bottomsquares.append(pygame.Vector2(math.floor(tl.x + i), math.floor(br.y)))

            for square in topsquares:
                if grid[int(square.x)][int(square.y)] != 0:
                    self.colliding = True
                    overlap = self.pos.y - self.size.y / 2 - (square.y + 1)

                    corner = False
                    break

            for square in bottomsquares:
                if grid[int(square.x)][int(square.y)] != 0:
                    self.colliding = True
                    overlap = self.pos.y + self.size.y / 2 - square.y

                    corner = False
                    break

        if overlap != 0:
            return overlap + overlap * self.stopthingsbreaking / abs(overlap), corner
        return overlap, corner

    def tilecollisions(self, grid, gravity, dt):
        overlap = pygame.Vector2()  # initialising empty variable

        gridpos = [int(self.pos.x), int(self.pos.y)]  # what cell the player is currently in. int for ease

        # check if center is inside a block i think it will squish here. need to look out for bugs
        if grid[gridpos[0]][gridpos[1]] != 0:
            self.colliding = True
            #return
        else:
            self.colliding = False

        # check if each surrounding cell is solid, and check if there is any overlap with that cell.

        if gravity.x == 0:
            self.pos.x += self.vel.x * dt
            overlap.x, corner = self.axistilecollisions(grid, 0, gravity)

            if corner == False:
                self.pos.x -= overlap.x
            else:
                self.pos.y -= gravity.y / abs(gravity.y)

            self.pos.y += self.vel.y * dt
            overlap.y, _ = self.axistilecollisions(grid, 1, gravity)
            self.pos.y -= overlap.y

        elif gravity.y == 0:
            self.pos.y += self.vel.y * dt
            overlap.y, corner = self.axistilecollisions(grid, 1, gravity)

            if corner == False:
                self.pos.y -= overlap.y
            else:
                self.pos.x -= gravity.x / abs(gravity.x)

            self.pos.x += self.vel.x * dt
            overlap.x, _ = self.axistilecollisions(grid, 0, gravity)
            self.pos.x -= overlap.x

        else:
            self.pos.x += self.vel.x * dt
            overlap.x, _ = self.axistilecollisions(grid, 0, gravity)
            self.pos.x -= overlap.x

            self.pos.y += self.vel.y * dt
            overlap.y, _ = self.axistilecollisions(grid, 1, gravity)
            self.pos.y -= overlap.y

            corner = False

        if corner == False:
            if overlap.x != 0:
                self.vel.x = 0
            if overlap.y != 0:
                self.vel.y = 0

        if overlap.y * gravity.y > 0 or overlap.x * gravity.x > 0:
            self.grounded = True
        else:
            self.grounded = False

    def updatephysics(self, movement, grid, gravity, dt):
        # MOVEMENT

        self.move += movement

        if gravity.length_squared() > 0:
            gravangle = math.atan2(gravity.x, gravity.y)
        else:
            gravangle = 0
        gravspacevel = self.vel.rotate_rad(gravangle)
        gravspacemove = self.move.rotate_rad(gravangle)

        if self.grounded:
            if gravspacemove.x:

                gravspacevel.x += gravspacemove.x * self.speed * self.accel / abs(gravspacemove.x)

                if gravspacevel.x > self.speed:
                    gravspacevel.x = self.speed
                elif gravspacevel.x < -self.speed:
                    gravspacevel.x = -self.speed
            else:

                if gravspacevel.x > self.deccel * self.speed:
                    gravspacevel.x -= self.speed * self.deccel
                elif gravspacevel.x < -self.deccel * self.speed:
                    gravspacevel.x += self.speed * self.deccel
                else:
                    gravspacevel.x = 0

            if gravspacemove.y < 0:
                gravspacevel.y = -self.jump
                self.grounded = False
        else:
            if gravspacemove.x:

                gravspacevel.x += gravspacemove.x * self.speed * self.airaccel / abs(gravspacemove.x)

                if gravspacevel.x > self.speed:
                    gravspacevel.x = self.speed
                elif gravspacevel.x < -self.speed:
                    gravspacevel.x = -self.speed
            else:

                if gravspacevel.x > self.airdeccel * self.speed:
                    gravspacevel.x -= self.speed * self.airdeccel
                elif gravspacevel.x < -self.airdeccel * self.speed:
                    gravspacevel.x += self.speed * self.airdeccel
                else:
                    gravspacevel.x = 0

        self.vel = gravspacevel.rotate_rad(-gravangle)

        self.vel += gravity  # idk where to put this. shouldnt change much though

        # COLLISIONS - includes position updates
        self.tilecollisions(grid, gravity, dt)  # check for collisions with the grid.
