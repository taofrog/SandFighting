import pygame

pygame.font.init()

class UIManager:
    def __init__(self, font):
        self.font = font

    def updateUIElement(self, screen, pos, text, colour=[255, 255, 255]):
        UIElement = self.font.render(text, True, colour)
        screen.blit(UIElement, pos)

