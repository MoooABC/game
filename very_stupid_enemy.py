import pygame, random
from enemy import enemy

class very_stupid_enemy(enemy):
    def __init__(self, x, y, size, movement):
        super().__init__(pygame.Vector2(x, y), size)
        self.MOVEMENT = movement

    def handel_movement(self):
        try:
            self.pos += self.MOVEMENT.normalize()
        except ValueError:
            pass

    def update(self, screen):
        screen_rect = screen.get_rect()
        self_rect =  pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

        if not screen_rect.colliderect(self_rect):
            return -1 # code for of screen
        return 0 # code for OK

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.pos.x, self.pos.y), self.size)

    def generate_enemy(W, H):
        r = 10
        return very_stupid_enemy(random.randint(r, W), random.choice([r, H-r]), r, pygame.math.Vector2(random.randint(-5, 7), random.randint(-7, 5)))