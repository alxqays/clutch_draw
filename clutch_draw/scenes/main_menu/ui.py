from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button


import pygame


def screen_main_menu(current_state, screen_width, screen_height, screen, font_apocalypse, title_text, events):
    play_button = create_button(font_apocalypse, "Play")
    options_button = create_button(font_apocalypse, "Options")
    credits_button = create_button(font_apocalypse, "Credits")
    exit_button = create_button(font_apocalypse, "Exit")
    screen.fill("purple")  # Fill the display with a solid color
    title_x = screen_width // 2 - title_text.get_width() // 2
    title_y = screen_height // 2 - title_text.get_height() // 2
    play_button_x = title_x
    play_button_y = title_y + 100
    options_button_x = title_x
    options_button_y = title_y + 200
    credits_button_x = title_x
    credits_button_y = title_y + 300
    exit_button_x = title_x
    exit_button_y = title_y + 400

    screen.blit(title_text, (title_x, title_y))
    screen.blit(play_button, (play_button_x, play_button_y))
    screen.blit(options_button, (options_button_x, options_button_y))
    screen.blit(credits_button, (credits_button_x, credits_button_y))
    screen.blit(exit_button, (exit_button_x, exit_button_y))

    for event in events:
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            if mouse_inside(event, play_button, play_button_x, play_button_y):
                current_state = GameState.GAME_SETUP_SCREEN
            if mouse_inside(event, options_button, options_button_x, options_button_y):
                current_state = GameState.OPTIONS_SCREEN
            if mouse_inside(event, credits_button, credits_button_x, credits_button_y):
                current_state = GameState.CREDITS_SCREEN
            if mouse_inside(event, exit_button, exit_button_x, exit_button_y):
                print("Exit clicked")
                pygame.quit()
                raise SystemExit

    return current_state