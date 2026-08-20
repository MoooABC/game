import pygame, sys, time, pygame_gui, os

from player import Player
from game_over import game_over
from very_stupid_enemy import very_stupid_enemy
from stupid_enemy import stupid_enemy
from archer_enemy import archer_enemy
from TNT_guy_enemy import TNT_guy_enemy

player = None
enemies = None
start_time = None
W, H = 1000, 700
min_respawn_distance = 300
screen = None


def reset(player_size=50):
    global player, enemies, start_time, W, H, screen, min_respawn_distance
    os.environ['SDL_VIDEO_WINDOW_POS'] = "center"
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("(-:")
    player = Player(W / 2, H / 2, player_size, 300)
    enemies = [stupid_enemy.generate_enemy(W, H, player, min_respawn_distance) for _ in range(4)] + \
              [very_stupid_enemy.generate_enemy(W, H) for _ in range(10)] + \
              [archer_enemy.generate_enemy(W, H, player, min_respawn_distance) for _ in range(5)] + \
              [TNT_guy_enemy.generate_enemy(W, H) for _ in range(4)]
    start_time = time.time()


reset()

ui_manager = pygame_gui.UIManager(
    (800, 600),
    theme_path="theme.json"
)
label_time = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 0), (100, 100)),
    text=f"000.0s",
    manager=ui_manager
)

clock = pygame.time.Clock()

while True:
    time_delta = clock.tick(120) / 1000.0
    player.reset_for_next_frame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        ui_manager.process_events(event)
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()
    player.update_for_attack(keys, time_delta, enemies, W, H)
    player.handle_movement(keys, W, H, time_delta)
    player.draw(screen, time_delta)

    for e in enemies[:]:
        match e.type:
            case "very_stupid_enemy":
                e.handle_movement(time_delta)
            case "stupid_enemy":
                e.handle_movement(player, time_delta)
            case "archer_enemy":
                e.handle_shoot(player, time_delta)
            case "TNT_guy_enemy":
                e.handle_shoot(time_delta, W, H, player)
            case _:
                raise RuntimeError("unknown enemy")
        if (e.check_collision_with_player(player)):
            temp_time = time.time() - start_time
            if temp_time < 0.5:
                print(e)
            p_size = game_over(time.time() - start_time)
            if p_size is not None:
                reset(p_size)
                break
            reset()
            break

        e.draw(screen, time_delta)
        if e.update(screen) == -1:
            enemies.remove(e)

            match e.type:
                case "very_stupid_enemy":
                    enemies.append(very_stupid_enemy.generate_enemy(W, H))
                case "stupid_enemy":
                    enemies.append(stupid_enemy.generate_enemy(W, H, player, min_respawn_distance))
                case "archer_enemy":
                    enemies.append(archer_enemy.generate_enemy(W, H, player, min_respawn_distance))
                case "TNT_guy_enemy":
                    enemies.append(TNT_guy_enemy.generate_enemy(W, H))

    label_time.set_text(str(round(time.time() - start_time, 1)))
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)

    pygame.display.set_caption(f"(-:\t{round(clock.get_fps(), 3)}fps")
    pygame.display.flip()
    pygame.display.update()
