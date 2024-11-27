
import pygame
import random
from typing import Dict
import math


class tile:
    def __init__(self, ID, colour):
        self.id = ID
        self.gravity = False
        self.sandPhysics = False
        self.colour = colour
        self.liquid = False
        self.gas = False
        self.temp = False
        self.displacingTiles = [0, 3]

class tileManager:
    def __init__(self, dimensions: tuple, tileTypes: Dict[int, tile]):
        self.tiles = [[0 for x in range(-1, dimensions[0] + 1)] for y in range(-1, dimensions[1] + 1)]
        self.updatedTiles = [[0 for x in range(-1, dimensions[0] + 1)] for y in range(-1, dimensions[1] + 1)]
        self.dimensions = dimensions
        self.tileTypes = tileTypes
        self.editSurf = pygame.surface.Surface(dimensions)
        self.scale = 16
        self.displaySurf = pygame.surface.Surface([dimensions[0] * self.scale, dimensions[0] * self.scale])
        self.showupdates = False
        self.sandmappng = pygame.image.load("Assets/SandMap.png")
        self.watermappng = pygame.image.load("Assets/WaterMap.png")
        self.explosionmappng = pygame.image.load("Assets/ExplosionMap.png")
        self.blockmappng = pygame.image.load("Assets/BlockMap.png")
        self.wateroffset = 0
        self.wateroffsetint = 0

    def update(self):
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                self.updatedTiles[x][y] = 0

        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                if y % 2 == 0:
                    x = self.dimensions[0] - x - 1
                if self.updatedTiles[x][y] == 0:
                    currentTile = self.tileTypes[self.tiles[x][y]]

                    if y + 1 < self.dimensions[1]:
                        if currentTile.temp:
                            prob = 0.2 + (y / 1024)
                            i = random.randint(0, 100) / 100
                            if i < prob:

                                self.tiles[x][y] = 0
                                self.updatedTiles[x][y] = 1
                            else:
                                if y - 1 >= 0:
                                    if self.tiles[x][y - 1] == 0:
                                        self.tiles[x][y - 1] = currentTile.id
                                        self.tiles[x][y] = 0
                                        self.updatedTiles[x][y - 1] = 1

                        if currentTile.gravity:
                            if self.tiles[x][y + 1] in currentTile.displacingTiles:
                                self.tiles[x][y] = self.tiles[x][y + 1]
                                self.updatedTiles[x][y] = 1
                                self.tiles[x][y + 1] = currentTile.id
                                self.updatedTiles[x][y + 1] = 1

                            elif currentTile.sandPhysics or currentTile.liquid:
                                directions = []

                                if x - 1 >= 0:
                                    if self.tiles[x - 1][y + 1] in currentTile.displacingTiles and \
                                            self.updatedTiles[x - 1][y + 1] == 0:
                                        directions.append(-1)

                                if x + 1 < self.dimensions[0]:
                                    if self.tiles[x + 1][y + 1] in currentTile.displacingTiles and \
                                            self.updatedTiles[x + 1][y + 1] == 0:
                                        directions.append(1)

                                if directions != []:
                                    chosenDirection = random.choice(directions)
                                    self.tiles[x][y] = self.tiles[x + chosenDirection][y + 1]
                                    self.updatedTiles[x][y] = 1
                                    self.tiles[x + chosenDirection][y + 1] = currentTile.id
                                    self.updatedTiles[x + chosenDirection][y + 1] = 1

                                elif currentTile.liquid:
                                    left = 0
                                    right = 0
                                    l = 1
                                    r = 1
                                    while x - l >= 0 and l != 0:
                                        if self.tiles[x - l][y + 1] != 3:
                                            if self.tiles[x - l][y + 1] != 0:
                                                break
                                            else:
                                                left = l
                                                break
                                        elif self.tiles[x - l][y] != 0:
                                            break
                                        l += 1

                                    while x + r < self.dimensions[0] and r != 0:

                                        if self.tiles[x + r][y + 1] != currentTile.id:
                                            if self.tiles[x + r][y + 1] != 0:
                                                break
                                            else:
                                                right = r
                                                break
                                        elif self.tiles[x + r][y] != 0:
                                            break
                                        r += 1

                                    if left > 0 or right > 0:
                                        if left < right and left != 0:
                                            direction = -left
                                        elif right < left and right != 0:
                                            direction = right
                                        else:
                                            dlist = [-left, right]
                                            direction = random.choice(dlist)

                                        if direction != 0:
                                            self.tiles[x][y] = self.tiles[x + direction][y + 1]
                                            self.updatedTiles[x][y] = 1
                                            self.tiles[x + direction][y + 1] = currentTile.id
                                            self.updatedTiles[x + direction][y + 1] = 1



    def updateSurf(self, screensize):
        self.wateroffset += 0.1
        self.wateroffsetint = math.floor(self.wateroffset)

        minscreen = min(screensize[0], screensize[1])
        scale = minscreen/64

        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if self.tiles[x][y] == 1:
                    colour = self.sandmappng.get_at((x, y))
                elif self.tiles[x][y] == 2:
                    colour = self.blockmappng.get_at((x, y))
                elif self.tiles[x][y] == 3:
                    colour = self.watermappng.get_at(((x + self.wateroffsetint) % 64, y))
                elif self.tiles[x][y] == 4:
                    colour = self.explosionmappng.get_at((x, y))
                else:
                    colour = self.tileTypes[self.tiles[x][y]].colour
                self.editSurf.set_at((x, y), colour)
                if self.showupdates and self.updatedTiles[x][y] != 0:
                    self.editSurf.set_at((x, y), [255,255,255,100])

        self.displaySurf = pygame.transform.scale_by(self.editSurf, scale)
