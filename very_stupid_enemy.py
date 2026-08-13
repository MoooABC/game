import pygame, random
from enemy import enemy
from SpriteSheet import SpriteSheet

class very_stupid_enemy(enemy):
    run_sprite_sheet = SpriteSheet("assets/images/very_stupid_enemy_run.png")
    frames_run = [
        run_sprite_sheet.get_image(0, 192, 192),
        run_sprite_sheet.get_image(192, 192, 192),
        run_sprite_sheet.get_image(384, 192, 192),
        run_sprite_sheet.get_image(576, 192, 192),
        run_sprite_sheet.get_image(768, 192, 192),
        run_sprite_sheet.get_image(960, 192, 192)
    ]
    def __init__(self, x, y, size, movement, speed):
        super().__init__(pygame.Vector2(x, y), size, "very_stupid_enemy")
        self.MOVEMENT = movement
        self.speed = speed

        self._timer_per_frame = 0.07
        self._timer = 0
        self._index = 0

    def handle_movement(self, delta_time):
        try:
            self.pos += (self.MOVEMENT.normalize() * self.speed * delta_time)
        except ValueError:
            pass

    def draw(self, screen, delta_time):
        self._timer += delta_time
        if self._timer >= self._timer_per_frame:
            self._timer = 0
            self._index += 1

        current_image = self.frames_run[self._index % len(self.frames_run)].convert_alpha()
        if self.MOVEMENT.x < 0:
            current_image = pygame.transform.flip(current_image, True, False)

        scaled_image = pygame.transform.scale(current_image, (self.size * 2.75, self.size * 2.75))
        tight_rect = scaled_image.get_bounding_rect()

        trimmed_image = pygame.Surface(tight_rect.size, pygame.SRCALPHA)
        trimmed_image.blit(scaled_image, (0, 0), tight_rect)

        screen.blit(trimmed_image, (self.pos.x, self.pos.y))

    def generate_enemy(W, H):
        r = 40
        return very_stupid_enemy(random.randint(r, W), random.choice([r, H-r]), r, pygame.math.Vector2(random.random(), random.random()), random.randint(70, 120))