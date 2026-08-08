import pygame, sys
from player import Player
from very_stupid_enemy import very_stupid_enemy

W, H = 800, 600
screen = pygame.display.set_mode((W, H))

pygame.display.set_caption("(-:")
clock = pygame.time.Clock()


player = Player(W/2, H/2, 10, 10)
enemies = [very_stupid_enemy.generate_enemy(W, H) for _ in range(10)]

while True:
    player.reset_for_next_frame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()

    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()
    player.handel_movement(keys)
    player.draw(screen)

    for e in enemies:
        e.handel_movement()
        if (e.check_collision_with_player(player)):
            print("Game Over")
            pygame.quit()
            sys.exit()

        e.draw(screen)
        if e.update(screen) == -1:
            enemies.remove(e)
            del e
            enemies.append(very_stupid_enemy.generate_enemy(W, H))


    pygame.display.flip()

    clock.tick(60)