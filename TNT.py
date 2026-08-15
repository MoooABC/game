import pygame, random, math
from SpriteSheet import SpriteSheet

class TNT:
    TNT_sprite = SpriteSheet("assets/images/objects/Dynamite.png")
    TNT_img =  TNT_sprite.get_image(0, 0, 64, 64)
    explode_sprite_sheet = SpriteSheet("assets/images/effects/Explosion_02.png")
    frames_explode = [
        explode_sprite_sheet.get_image(0, 0, 192, 192),
        explode_sprite_sheet.get_image(192, 0, 192, 192),
        explode_sprite_sheet.get_image(384, 0, 192, 192),
        explode_sprite_sheet.get_image(576, 0, 192, 192),
        explode_sprite_sheet.get_image(768, 0, 192, 192),
        explode_sprite_sheet.get_image(960, 0, 192, 192),
        explode_sprite_sheet.get_image(1152, 0, 192, 192),
        explode_sprite_sheet.get_image(1344, 0, 192, 192),
        explode_sprite_sheet.get_image(1536, 0, 192, 192),
        explode_sprite_sheet.get_image(1728, 0, 192, 192)
    ]
    def __init__(self, x, y, direction, speed):
        self.pos = pygame.math.Vector2(x, y)
        self.rotation = 0
        self.direction = direction
        self.speed = speed
        self.size = self.TNT_img.get_size()
        self._timer = 0
        self._animation_index = 0
        self._life_time = 1
        self.exploding = False
        self.explode_distance = 5
        self.kill_player = False

    def check_collision(self, player):
        player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size, player.size)
        self_rect =  pygame.Rect(int(self.pos.x), int(self.pos.y), self.size[0], self.size[1])
        return player_rect.colliderect(self_rect) or self.kill_player

    def update(self, delta_time, player):
        if self.exploding:
            distance = math.sqrt((self.pos.x - player.pos.x)**2+(self.pos.y - player.pos.y)**2)
            if distance <= self.explode_distance:
                self.kill_player = True
            return -1
        self._timer += delta_time
        velocity = self.direction * self.speed * delta_time
        self.pos += velocity
        self.rotation += delta_time * 100

    def draw(self, screen):
        if self._timer >= self._life_time:
            try:
                current_image = self.frames_explode[self._animation_index]
                self._animation_index += 1
                screen.blit(current_image, self.pos)
            except IndexError:
                self.exploding = True
            return
        rotated_image = pygame.transform.rotate(self.TNT_img, self.rotation)
        screen.blit(rotated_image, self.pos)