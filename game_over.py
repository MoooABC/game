import pygame
import pygame_gui
from tkinter import messagebox
import sys

def game_over(time):
    pygame.init()

    pygame.mouse.set_visible(False)
    img_cursor_default = pygame.image.load("assets/images/cursors/Cursor_default.png").convert_alpha()
    img_cursor_pointer = pygame.image.load("assets/images/cursors/Cursor_pointer.png").convert_alpha()
    img_cursor_text = pygame.image.load("assets/images/cursors/Cursor_text.png").convert_alpha()
    img_cursor_forbidden = pygame.image.load("assets/images/cursors/Cursor_forbidden.png").convert_alpha()


    window_surface = pygame.display.set_mode((800, 600), pygame.NOFRAME)
    pygame.display.set_caption("Game Over")

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#282c34'))

    ui_manager = pygame_gui.UIManager(
        (800, 600),
        theme_path="theme.json"
    )
    lang = ui_manager.get_locale() # unsupported languages will teat as eng

    label_lose = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 250), (120, 40)),
        text= "הפסדת!" if lang == "he" else "You lost!",
        manager=ui_manager,
        object_id="text_lose"
    )
    label_lose.hovering_allowed = True
    label_feedback = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 270), (240, 50)),
        text= ("אתה תבוסתן!" if time < 10 else "אתה יכול לעשות טוב יותר" if time < 100 else "נהדר") if lang=="he" else ("you are a loser!" if time < 10 else "you can do better" if time < 100 else "geat! :)"),
        manager=ui_manager,
        object_id="text_feedback"
    )
    label_feedback.hovering_allowed = True
    button_play_again = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 340), (150, 50)),
        text= "שחק שוב" if lang=="he" else "play again",
        manager=ui_manager,
        object_id="button_play_again"
    )
    button_exit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 400), (150, 50)),
        text= "יציאה" if lang=="he" else "exit",
        manager=ui_manager,
        object_id="button_exit"
    )
    button_debug = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 480), (150, 50)),
        text= "debug data",
        manager=ui_manager,
        object_id="forbidden_debug"
    )

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        current_cursor = img_cursor_default
        if ui_manager.get_hovering_any_element():
            hovered_element = None
            mouse_pos = ui_manager.get_mouse_position()
            for element in ui_manager.get_sprite_group().sprites():
                if isinstance(element, pygame_gui.core.UIContainer):
                    continue
                if element.hover_point(mouse_pos[0], mouse_pos[1]):
                    hovered_element = element
                    break
            if hovered_element:
                element_id = hovered_element.most_specific_combined_id
                if "forbidden" in element_id:
                    current_cursor = img_cursor_forbidden
                elif "button" in element_id:
                    current_cursor = img_cursor_pointer
                elif "text" in element_id:
                    current_cursor = img_cursor_text

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            ui_manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_play_again:
                    is_running = False
                elif event.ui_element == button_exit:
                    pygame.quit()
                    sys.exit()
                elif event.ui_element == button_debug:
                    text_list = [f"id: {e.most_specific_combined_id}  txt: {e.text}" for e in ui_manager.get_sprite_group().sprites() if
                                 not isinstance(e, pygame_gui.core.UIContainer)]
                    messagebox.showinfo("debug message", f"language: {lang}\n" +
                                                         f"FPS: {clock.get_fps()}\n" +
                                                         f"dt: {time_delta}\n\n\n" +
                                                         f"elements:\n {"\n".join(text_list)}")


        ui_manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        ui_manager.draw_ui(window_surface)

        mouse_pos = pygame.mouse.get_pos()
        window_surface.blit(current_cursor, mouse_pos)

        pygame.display.flip()
        pygame.display.update()
    pygame.mouse.set_visible(True)