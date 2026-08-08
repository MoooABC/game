import pygame, random
from enemy import enemy

class stupid_enemy(enemy):
    def __init__(self, x, y, size, speed):
        super().__init__(pygame.Vector2(x, y), size, "stupid_enemy")
        self.SPEED = speed

    def handle_movement(self, player):
        self.pos += (player.pos - self.pos) * self.SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.pos.x, self.pos.y), self.size)

    def generate_enemy(W:int, H:int):
        r = 10
        return stupid_enemy(random.randint(r, W), random.choice([r, H-r]), r, 0.015)