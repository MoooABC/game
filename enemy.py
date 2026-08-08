from abc import ABC, abstractmethod
import pygame

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
        player_rect = pygame.Rect(player.pos.x-player.size, player.pos.y-player.size, player.size*2, player.size*2)
        self_rect =  pygame.Rect(self.pos.x-self.size, self.pos.y-self.size, self.size*2, self.size*2)
        if player_rect.colliderect(self_rect):
            return True
        return False