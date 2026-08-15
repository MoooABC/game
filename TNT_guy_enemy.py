import pygame, random
import player
from TNT import TNT
from enemy import enemy
from SpriteSheet import SpriteSheet


class TNT_guy_enemy(enemy):

    sprite_sheet = SpriteSheet("assets/images/enemies/TNT_guy/TNT_Red.png")
    frames_idle = [
        sprite_sheet.get_image(0, 0, 192, 192),
        sprite_sheet.get_image(192, 0, 192, 192),
        sprite_sheet.get_image(384, 0, 192, 192),
        sprite_sheet.get_image(576, 0, 192, 192),
        sprite_sheet.get_image(768, 0, 192, 192),
        sprite_sheet.get_image(960, 0, 192, 192)
    ]
    frames_shoot = [
        sprite_sheet.get_image(0, 384,192, 192),
        sprite_sheet.get_image(192, 384,192, 192),
        sprite_sheet.get_image(384, 384, 192, 192),
        sprite_sheet.get_image(576, 384, 192, 192),
        sprite_sheet.get_image(768, 384, 192, 192),
        sprite_sheet.get_image(960, 384, 192, 192),
        sprite_sheet.get_image(1152, 384, 192, 192)
    ]

    def __init__(self, x, y, size, time_per_shot):
        super().__init__(pygame.Vector2(x, y), size, "TNT_guy_enemy")

        self.isShooting = False
        self._timer_per_shot = time_per_shot
        self._timer_shoot = 0
        self._timer_per_frame = 0.07
        self._timer_animation = 0
        self._index = 0
        self.current_TNTs = []

        self.player_position = None


    def check_collision_with_player(self, player):
        player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size, player.size)
        self_rect =  pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        if player_rect.colliderect(self_rect):
            return True
        for TNT in self.current_TNTs:
            if TNT.check_collision(player):
                return True
        return False

    def handle_shoot(self, delta_time, W, H, player):
        if not self.isShooting:
            self._timer_shoot += delta_time
            if self._timer_shoot >= self._timer_per_shot:
                self._index = 0
                self._timer_shoot = 0
                self._timer_animation = 0
                self.isShooting = True

                corners = {
                    "top_left": pygame.math.Vector2(0, 0),
                    "top_right": pygame.math.Vector2(W, 0),
                    "bottom_left": pygame.math.Vector2(0, H),
                    "bottom_right": pygame.math.Vector2(W, H)
                }
                farthest_corner_pos = corners[max(corners, key=lambda c: self.pos.distance_to(corners[c]))]
                vec = farthest_corner_pos - self.pos
                dir_vector = pygame.math.Vector2(random.uniform(-5, 5), random.uniform(-5, 5)) + vec
                dir_vector = dir_vector.normalize()
                self.current_TNTs.append(TNT(self.pos.x, self.pos.y, dir_vector, 170))

        for t in self.current_TNTs[:]:
             if t.update(delta_time, player) == -1:
                self.current_TNTs.remove(t)
                del t

        if (self._index >= len(self.frames_shoot)):
            self.isShooting = False


    def draw(self, screen, delta_time):
        self._timer_animation += delta_time
        if self._timer_animation >= self._timer_per_frame:
            self._timer_animation = 0
            self._index += 1

        if self.isShooting:
            current_image = self.frames_shoot[self._index % len(self.frames_shoot)].convert_alpha()
        else:
            current_image = self.frames_idle[self._index % len(self.frames_idle)].convert_alpha()
        scaled_image = pygame.transform.scale(current_image, (self.size*2.75, self.size*2.75))
        tight_rect = scaled_image.get_bounding_rect()

        trimmed_image = pygame.Surface(tight_rect.size, pygame.SRCALPHA)
        trimmed_image.blit(scaled_image, (0, 0), tight_rect)

        for TNT in self.current_TNTs:
            TNT.draw(screen)
        screen.blit(trimmed_image, (self.pos.x, self.pos.y))

    def generate_enemy(W:int, H:int):
        r = 40
        return TNT_guy_enemy(random.randint(r, W), random.choice([r, H-r]), r, (random.random()+0.1) * 4)