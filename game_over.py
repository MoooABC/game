import pygame
import pygame_gui
import sys

def game_over(time):
    pygame.init()

    pygame.mouse.set_visible(False)
    img_cursor_default = pygame.image.load("assets/images/Cursor_default.png").convert_alpha()
    img_cursor_pointer = pygame.image.load("assets/images/Cursor_pointer.png").convert_alpha()
    #img_text = pygame.image.load("assets/images/Cursor_text.png").convert_alpha()
    img_forbidden = pygame.image.load("assets/images/Cursor_forbidden.png").convert_alpha()


    window_surface = pygame.display.set_mode((800, 600), pygame.NOFRAME)
    pygame.display.set_caption("Game Over")

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#282c34'))

    ui_manager = pygame_gui.UIManager(
        (800, 600),
        theme_path="theme.json"
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
    button_play_again = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 340), (150, 50)),
        text= "play again",
        manager=ui_manager
    )
    button_exit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 400), (150, 50)),
        text= "exit",
        manager=ui_manager
    )


    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        current_cursor = img_cursor_default
        if ui_manager.get_hovering_any_element():
            current_cursor = img_cursor_pointer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            ui_manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_play_again:
                    is_running = False
                if event.ui_element == button_exit:
                    pygame.quit()
                    sys.exit()
        ui_manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        ui_manager.draw_ui(window_surface)

        mouse_pos = pygame.mouse.get_pos()
        window_surface.blit(current_cursor, mouse_pos)

        pygame.display.flip()
        pygame.display.update()