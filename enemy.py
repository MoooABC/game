from abc import ABC, abstractmethod
import pygame, random

class enemy(ABC):
    def __init__(self, pos, size, type):
        self.pos = pos
        self.size = size
        self.type = type

    @staticmethod
    @abstractmethod
    def generate_enemy(W : int, H : int) -> enemy:
        pass

    def update(self, screen):
        screen_rect = screen.get_rect()
        self_rect =  pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

        if not screen_rect.colliderect(self_rect):
            return -1 # code for of screen
        return 0 # code for OK


    def update(self, screen):
        screen_rect = screen.get_rect()
        self_rect =  pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

        if not screen_rect.colliderect(self_rect):
            return -1 # code for of screen
        return 0 # code for OK


    @abstractmethod
    def draw(self, screen) -> None:
        pass


    def check_collision_with_player(self, player):
        player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size, player.size)
        size_shrink = 0.5
        new_size = self.size * size_shrink
        offset = (self.size - new_size) / 2
        self_rect = pygame.Rect(self.pos.x + offset, self.pos.y + offset, new_size, new_size)

        return player_rect.colliderect(self_rect)