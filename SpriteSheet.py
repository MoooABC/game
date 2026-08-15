import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, frame_x, frame_y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (frame_x, frame_y, width, height))
        return image