import pygame
import math

pygame.font.init()

class UIManager:
    def __init__(self, font, size):
        self.font = "Arial"
        self.size = size

    def updateUIElement(self, screen, scale, offsetx, offsety, pos, text, colour=[255, 255, 255]):
        font = pygame.font.SysFont(self.font, math.floor(self.size * scale / 12))

        finalpos = pygame.Vector2(pos[0], pos[1])
        finalpos *= scale

        UIElement = font.render(text, True, colour)
        screen.blit(UIElement, finalpos + pygame.Vector2(offsetx, offsety))

