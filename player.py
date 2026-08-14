import random

import pygame
import math
from SpriteSheet import SpriteSheet

pygame.init()

class Player:
    run_sprite_sheet = SpriteSheet("assets/images/player/Player_run.png")
    frames_run = [
        run_sprite_sheet.get_image(0, 192, 192),
        run_sprite_sheet.get_image(192, 192, 192),
        run_sprite_sheet.get_image(384, 192, 192),
        run_sprite_sheet.get_image(576, 192, 192),
        run_sprite_sheet.get_image(768, 192, 192),
        run_sprite_sheet.get_image(960, 192, 192)
    ]
    idle_sprite_sheet = SpriteSheet("assets/images/player/Player_Idle.png")
    frames_idle = [
        idle_sprite_sheet.get_image(0, 192, 192),
        idle_sprite_sheet.get_image(192, 192, 192),
        idle_sprite_sheet.get_image(384, 192, 192),
        idle_sprite_sheet.get_image(576, 192, 192),
        idle_sprite_sheet.get_image(768, 192, 192),
        idle_sprite_sheet.get_image(960, 192, 192),
        idle_sprite_sheet.get_image(1152, 192, 192),
        idle_sprite_sheet.get_image(1344, 192, 192)
    ]
    attack_sprite_sheet = SpriteSheet("assets/images/player/Player_attack.png")
    frames_attack = [
        attack_sprite_sheet.get_image(0, 192, 192),
        attack_sprite_sheet.get_image(192, 192, 192),
        attack_sprite_sheet.get_image(384, 192, 192),
        attack_sprite_sheet.get_image(576, 192, 192)
    ]
    def __init__(self, x, y, size, speed):
        self.pos = pygame.Vector2(x, y)
        self.size = size
        self.movement = pygame.math.Vector2(0, 0)
        self.SPEED = speed

        self.isRunning = False
        self._timePerFrame = 0.07
        self._timer_animation = 0
        self._index = 0

        self.isAttacking = False
        self._attack_time = 0.95
        self._timer_attack = 0
        self._attack_distance = 110

    def reset_for_next_frame(self):
        self.movement = pygame.math.Vector2()

    def update_for_attack(self, pressed_keys, delta_time, enemies, W, H):
        self._timer_attack += delta_time

        if pressed_keys[pygame.K_SPACE] and self._timer_attack >= self._attack_time:
            self._timer_attack = 0
            self._index = 0
            self.isAttacking = True
            for e in enemies:
                distance = math.sqrt(math.pow(self.pos.x - e.pos.x, 2) + math.pow(self.pos.y - e.pos.y, 2))
                if distance <= self._attack_distance:
                    e.pos = pygame.math.Vector2(random.randint(self.size, W-self.size), -random.randint(self.size, H-self.size)) # send the enemy of screen so it will respawn
                    # i used random place of screen and not just (-10;-10) because somehow it made all the enemies respawn in the top left corner

    def handle_movement(self, pressed_keys, W, H, delta_time):
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.movement.x -= 1
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.movement.x += 1
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.movement.y -= 1
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.movement.y += 1

        if self.movement.length_squared() > 0:
            self.isRunning = True
            temp_pos = self.pos + (self.movement.normalize() * self.SPEED * delta_time)
            if temp_pos.x < 0:
                temp_pos.x = 0
            elif temp_pos.x > W - self.size:
                temp_pos.x = W - self.size

            if temp_pos.y < 0:
                temp_pos.y = 0
            elif temp_pos.y > H - self.size:
                temp_pos.y = H - self.size

            self.pos = temp_pos
        else:
            self.isRunning = False

    def draw(self, screen, delta_time):
        self._timer_animation += delta_time
        if self._timer_animation >= self._timePerFrame:
            self._timer_animation = 0
            self._index += 1

        if self.isAttacking:
            try:
                current_image = self.frames_attack[self._index].convert_alpha()
            except IndexError:
                current_image = self.frames_idle[self._index % len(self.frames_idle)].convert_alpha()
                self.isAttacking = False
            finally:
                if self.movement.x < 0:
                    current_image = pygame.transform.flip(current_image, True, False)
        elif self.isRunning:
            current_image = self.frames_run[self._index % len(self.frames_run)].convert_alpha()
            if self.movement.x < 0:
                current_image = pygame.transform.flip(current_image, True, False)
        else:
            current_image = self.frames_idle[self._index % len(self.frames_idle)].convert_alpha()
        scaled_image = pygame.transform.scale(current_image, (self.size*2.75, self.size*2.75))
        tight_rect = scaled_image.get_bounding_rect()

        trimmed_image = pygame.Surface(tight_rect.size, pygame.SRCALPHA)
        trimmed_image.blit(scaled_image, (0, 0), tight_rect)

        screen.blit(trimmed_image, (self.pos.x, self.pos.y))