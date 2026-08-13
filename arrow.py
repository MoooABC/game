import pygame, random, math

class arrow():
    arrow_img = pygame.image.load("assets/images/arrow.png").convert_alpha()
    def __init__(self, x, y, direction, speed, player):
        self.pos = pygame.math.Vector2(x, y)
        dx = self.pos.x - player.pos.x
        dy = self.pos.y - player.pos.y
        self.rotation = math.degrees(math.atan2(dy, -dx))
        self.direction = direction
        self.speed = speed
        self.size = self.arrow_img.get_size()
        self._life_time = 3
        self._timer = 0

    def check_collision(self, player):
        player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size, player.size)
        self_rect =  pygame.Rect(int(self.pos.x), int(self.pos.y), self.size[0], self.size[1])
        return player_rect.colliderect(self_rect)

    def update(self, delta_time):
        self._timer += delta_time
        if self._timer > self._life_time:
            return False
        velocity = self.direction * self.speed * delta_time
        self.pos += velocity
        return True

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.arrow_img, self.rotation)
        screen.blit(rotated_image, self.pos)