import pygame, sys, time, pygame_gui

from player import Player
from very_stupid_enemy import very_stupid_enemy
from game_over import game_over

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("(-:")

ui_manager = pygame_gui.UIManager(
    (800, 600),
    theme_path={"label": {"font": {"name": "arial", "size": "30"}}}
)
label_time = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 0), (100, 100)),
    text= f"000.0s",
    manager=ui_manager
)

clock = pygame.time.Clock()
player = None
enemies = None
start_time = None

def reset():
    global player, enemies, start_time
    player = Player(W/2, H/2, 10, 5)
    enemies = [very_stupid_enemy.generate_enemy(W, H) for _ in range(40)]
    start_time = time.time()

reset()
while True:
    time_delta = clock.tick(60) / 1000.0
    player.reset_for_next_frame()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()
        ui_manager.process_events(event)
    screen.fill((255, 255, 255))
    label_time.set_text(str(round(time.time()-start_time, 1)))
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)

    keys = pygame.key.get_pressed()
    player.handel_movement(keys)
    player.draw(screen)

    for e in enemies:
        e.handel_movement()
        if (e.check_collision_with_player(player)):
            game_over(time.time()-start_time)
            reset()

        e.draw(screen)
        if e.update(screen) == -1:
            enemies.remove(e)
            del e
            enemies.append(very_stupid_enemy.generate_enemy(W, H))


    pygame.display.flip()
    pygame.display.update()