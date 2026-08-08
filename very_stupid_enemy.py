import pygame, random
from enemy import enemy

class very_stupid_enemy(enemy):
    def __init__(self, x, y, size, movement):
        super().__init__(pygame.Vector2(x, y), size, "very_stupid_enemy")
        self.MOVEMENT = movement

    def handle_movement(self):
        try:
            self.pos += self.MOVEMENT.normalize()
        except ValueError:
            pass


    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.pos.x, self.pos.y), self.size)

    def generate_enemy(W, H):
        r = 10
        return very_stupid_enemy(random.randint(r, W), random.choice([r, H-r]), r, pygame.math.Vector2(random.randint(-5, 7), random.randint(-7, 5)))