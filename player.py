import pygame

class Player:
    def __init__(self, x, y, size, speed):
        self.pos = pygame.Vector2(x, y)
        self.size = size
        self.movement = pygame.math.Vector2(0, 0)
        self.SPEED = speed

    def reset_for_next_frame(self):
        self.movement = pygame.math.Vector2()

    def handle_movement(self, pressed_keys, W, H):
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.movement.x -= self.SPEED
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.movement.x += self.SPEED
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.movement.y -= self.SPEED
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.movement.y += self.SPEED
        try:
            temp_pos = self.pos + (self.movement.normalize() * self.SPEED)
            if temp_pos.x < self.size: temp_pos.x = self.size;
            elif temp_pos.x > W - self.size: temp_pos.x = W - self.size;
            if temp_pos.y < self.size: temp_pos.y = self.size;
            elif temp_pos.y > H - self.size: temp_pos.y = H - self.size;

            self.pos = temp_pos
        except ValueError:
            pass

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.pos.x, self.pos.y), self.size)