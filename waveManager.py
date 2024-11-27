import pygame
import random
import math
from Enemy import enemy

waveamounts = {1: 1,
               2: 2,
               3: 5,
               4: 7,
               5: 10,
               6: 15,
               7: 20,
               8: 50,
               9: 75,
               10:100}


class wavemanager:
    def __init__(self, *args: enemy):
        self.enemies = [fellow for fellow in args]
        self.wave = 1
        self.enemieskilled = 0
        self.totalkills = 0

    def spawnenemy(self, grid, player):
        x = random.randint(1, 62)

        self.enemies.append(enemy(60, 10, 2.2, 2.2, 100/(self.wave + 6), 0.03, 0.008, 40, "blockgun"))

    def update(self, grid, player):
        if self.enemieskilled >= waveamounts[self.wave]:
            self.wave += 1
            self.enemieskilled = 0

        rand = random.randint(0, 100000) / 100000
        if waveamounts[self.wave]/2500 >= rand:
            self.spawnenemy(grid, player)

    def updateenemies(self, player, manager, gravity, dt):
        for fellow in self.enemies:
            if fellow.update(player, manager.tiles, gravity, dt, manager):
                self.enemies.remove(fellow)
                self.enemieskilled += 1
                self.totalkills += 1

    def drawenemies(self, screen, screensize, offsetx, offsety):
        for fellow in self.enemies:
            fellow.draw(screen, screensize, offsetx, offsety)
