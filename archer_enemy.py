import pygame, random, math

from arrow import arrow
from enemy import enemy
from SpriteSheet import SpriteSheet


class archer_enemy(enemy):
    shoot_sprite_sheet = SpriteSheet("assets/images/enemies/archer/Archer_Shoot.png")
    frames_shoot = [
        shoot_sprite_sheet.get_image(0, 192, 192),
        shoot_sprite_sheet.get_image(192, 192, 192),
        shoot_sprite_sheet.get_image(384, 192, 192),
        shoot_sprite_sheet.get_image(576, 192, 192),
        shoot_sprite_sheet.get_image(768, 192, 192),
        shoot_sprite_sheet.get_image(960, 192, 192),
        shoot_sprite_sheet.get_image(1152, 192, 192),
        shoot_sprite_sheet.get_image(1344, 192, 192),
        shoot_sprite_sheet.get_image(1536, 192, 192)
    ]
    idle_sprite_sheet = SpriteSheet("assets/images/enemies/archer/Archer_Idle.png")
    frames_idle = [
        idle_sprite_sheet.get_image(0, 192, 192),
        idle_sprite_sheet.get_image(192, 192, 192),
        idle_sprite_sheet.get_image(384, 192, 192),
        idle_sprite_sheet.get_image(576, 192, 192),
        idle_sprite_sheet.get_image(768, 192, 192),
        idle_sprite_sheet.get_image(960, 192, 192),
    ]
    def __init__(self, x, y, size, time_per_shot):
        super().__init__(pygame.Vector2(x, y), size, "archer_enemy")

        self.isShooting = False
        self._timer_per_shot = time_per_shot
        self._timer_shoot = 0
        self._timer_per_frame = 0.07
        self._timer_animation = 0
        self._index = 0
        self.current_arrows = []

        self.player_position = None


    def check_collision_with_player(self, player):
        player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size, player.size)
        self_rect =  pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        if player_rect.colliderect(self_rect):
            return True
        for arrow in self.current_arrows:
            if arrow.check_collision(player):
                return True
        return False

    def handle_shoot(self, player, delta_time):
        self.player_position = player.pos
        if not self.isShooting:
            self._timer_shoot += delta_time
            if self._timer_shoot >= self._timer_per_shot:
                self._index = 0
                self._timer_shoot = 0
                self._timer_animation = 0
                self.isShooting = True

                dir_vector = player.pos - self.pos

                if dir_vector.length() > 0:
                    dir_vector = dir_vector.normalize()
                else:
                    dir_vector = pygame.math.Vector2(1, 0)
                self.current_arrows.append(arrow(self.pos.x, self.pos.y, dir_vector, 170, player))

        for a in self.current_arrows[:]:
            if not a.update(delta_time):
                self.current_arrows.remove(a)
                del a

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
        if self.player_position.x < self.pos.x:
            current_image = pygame.transform.flip(current_image, True, False)
        scaled_image = pygame.transform.scale(current_image, (self.size*2.75, self.size*2.75))
        tight_rect = scaled_image.get_bounding_rect()

        trimmed_image = pygame.Surface(tight_rect.size, pygame.SRCALPHA)
        trimmed_image.blit(scaled_image, (0, 0), tight_rect)

        for arrow in self.current_arrows:
            arrow.draw(screen)
        screen.blit(trimmed_image, (self.pos.x, self.pos.y))

    def generate_enemy(W:int, H:int):
        r = 40
        return archer_enemy(random.randint(r, W), random.choice([r, H-r]), r, (random.random()+0.08) * 7)