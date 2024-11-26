import pygame
import random
from typing import Dict


class tile:
    def __init__(self, ID, colour):
        self.id = ID
        self.gravity = False
        self.sandPhysics = False
        self.colour = colour
        self.liquid = False
        self.gas = False
        self.displacingTiles = [0]

class tileManager:
    def __init__(self, dimensions: tuple, tileTypes: Dict[int, tile]):
        self.tiles = [[0 for x in range(-1, dimensions[0] + 1)] for y in range(-1, dimensions[1] + 1)]
        self.updatedTiles = [[0 for x in range(dimensions[0])] for y in range(dimensions[1])]
        self.dimensions = dimensions
        self.tileTypes = tileTypes
        self.editSurf = pygame.surface.Surface(dimensions)
        self.scale = 16
        self.displaySurf = pygame.surface.Surface([dimensions[0] * self.scale, dimensions[0] * self.scale])

    def update(self):
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                if y % 2 == 0:
                    x = self.dimensions[0] - x - 1
                if self.updatedTiles[x][y] == 0:
                    currentTile = self.tileTypes[self.tiles[x][y]]

                    if y + 1 < self.dimensions[1]:
                        if currentTile.gravity:
                            if self.tiles[x][y + 1] in currentTile.displacingTiles:
                                self.tiles[x][y] = self.tiles[x][y + 1]
                                self.updatedTiles[x][y] = 1
                                self.tiles[x][y + 1] = currentTile.id
                                self.updatedTiles[x][y + 1] = 1
                                if currentTile.liquid:
                                    print("wetfall")

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
                                    displacements = [-1, 1]
                                    foundL = False
                                    foundR = False

                                    while x + displacements[0] >= 0:
                                        if self.tiles[x + displacements[0]][y] == 0:
                                            if self.tiles[x + displacements[0]][
                                                y + 1] in currentTile.displacingTiles and \
                                                    self.updatedTiles[x + displacements[0]][y + 1] == 0:
                                                foundL = True

                                                break
                                            displacements[0] -= 1
                                        else:
                                            break

                                    while x + displacements[1] < self.dimensions[0]:
                                        #print(x + displacements[1])

                                        if self.tiles[x + displacements[1]][y] == 0:
                                            if self.tiles[x + displacements[1]][
                                                y + 1] in currentTile.displacingTiles and \
                                                    self.updatedTiles[x + displacements[1]][y + 1] == 0:
                                                foundR = True
                                                break
                                            displacements[1] += 1
                                        else:
                                            break

                                    dir = 0


                                    if foundL and foundR:

                                        if abs(displacements[0]) > displacements[1]:
                                            dir = displacements[0]

                                        elif abs(displacements[1]) > displacements[0]:
                                            dir = displacements[1]

                                        else:
                                            dir = displacements[0]

                                    elif foundL:
                                        dir = displacements[0]

                                    elif foundR:
                                        dir = displacements[1]

                                    else:
                                        break

                                    self.tiles[x][y] = self.tiles[x + dir][y + 1]
                                    self.tiles[x + dir][y + 1] = currentTile.id
                                    self.updatedTiles[x][y] = 1
                                    self.updatedTiles[x + dir][y + 1] = 1


        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                self.updatedTiles[x][y] = 0

    def updateSurf(self, offsetX, offsetY):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                colour = self.tileTypes[self.tiles[x][y]].colour
                self.editSurf.set_at((x + offsetX, y + offsetY), colour)

        self.displaySurf = pygame.transform.scale_by(self.editSurf, self.scale)
