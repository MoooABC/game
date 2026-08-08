import pygame
import pygame_gui

def game_over(time):
    pygame.init()

    window_surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Over")

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#282c34'))

    ui_manager = pygame_gui.UIManager(
        (800, 600),
        theme_path={"label": {"font": {"name": "arial", "size": "30"}}}
    )

    label_lose = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 250), (200, 50)),
        text= f"You lost!",
        manager=ui_manager
    )

    label_feedback = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 270), (200, 70)),
        text= "you are a loser!" if time < 10 else "you can do better" if time < 100 else "geat! :)",
        manager=ui_manager
    )


    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(10) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            ui_manager.process_events(event)
        ui_manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        ui_manager.draw_ui(window_surface)

        pygame.display.update()