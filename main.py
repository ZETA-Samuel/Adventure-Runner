import asyncio
import os
import pygame
import game

pygame.init()


async def main():
    clock = pygame.time.Clock()
    base = os.path.dirname(__file__)

    def load_image(path):
        return pygame.image.load(os.path.join(base, path)).convert_alpha()

    MENU_SIZE = (1075, 580)
    display = pygame.display.Info()
    desktop_w = display.current_w or MENU_SIZE[0]
    desktop_h = display.current_h or MENU_SIZE[1]
    window = pygame.display.set_mode((min(1280, desktop_w), min(720, desktop_h)), pygame.RESIZABLE)
    screen = pygame.Surface(MENU_SIZE)
    pygame.display.set_caption("Menu")

    #image loading
    play_img = load_image("images/Menu/Buttons/Play.png")
    setting_img = load_image("images/Menu/Buttons/Settings.png")
    achievements_img = load_image("images/Menu/Buttons/Achievements.png")
    leaderboard_img = load_image("images/Menu/Buttons/Leaderboard.png")
    close_img = load_image("images/Menu/Buttons/Close.png")
    close_img = pygame.transform.scale(close_img, (23, 25))

    #background
    bg = pygame.image.load(os.path.join(base, "images/Background/anthropic.jpg")).convert()
    bg = pygame.transform.scale(bg, MENU_SIZE)
    change_bg = pygame.image.load(os.path.join(base, "images/Background/change_bg.jpg")).convert()
    change_bg = pygame.transform.scale(change_bg, MENU_SIZE)
    title_font = pygame.font.Font(os.path.join(base, "images/fonts/PixelOperator8-Bold.ttf"), 36)
    message_font = pygame.font.Font(os.path.join(base, "images/fonts/PixelOperator8.ttf"), 22)

    buttons = [
        ("Play", play_img, play_img.get_rect(topleft=(520.5, 386.67))),
        ("Settings", setting_img, setting_img.get_rect(topleft=(646.25, 386.67))),
        ("Achievements", achievements_img, achievements_img.get_rect(topleft=(251.75, 386.67))),
        ("Leaderboard", leaderboard_img, leaderboard_img.get_rect(topleft=(386.125, 386.67))),
        ("Close", close_img, close_img.get_rect(topleft=(772.25, 386.67))),
    ]

    #set_background
    screen.blit(bg, (0, 0))

    #main menu
    running = True
    under_construction = False

    def logical_pos(pos):
        window_w, window_h = window.get_size()
        scale = min(window_w / MENU_SIZE[0], window_h / MENU_SIZE[1])
        offset_x = (window_w - MENU_SIZE[0] * scale) / 2
        offset_y = (window_h - MENU_SIZE[1] * scale) / 2
        return ((pos[0] - offset_x) / scale, (pos[1] - offset_y) / scale)

    while running:
        mouse_pos = logical_pos(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                under_construction = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if under_construction:
                    under_construction = False
                else:
                    click_pos = logical_pos(event.pos)
                    for name, image, rect in buttons:
                        if rect.collidepoint(click_pos):
                            if name == "Play":
                                await game.run_game()
                                pygame.init()
                                window = pygame.display.set_mode(
                                    (min(1280, desktop_w), min(720, desktop_h)), pygame.RESIZABLE
                                )
                                pygame.display.set_caption("Menu")
                            elif name == "Close":
                                running = False
                            else:
                                under_construction = True
                            break

        if not under_construction and any(rect.collidepoint(mouse_pos) for name, image, rect in buttons):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if under_construction:
            screen.blit(change_bg, (0, 0))
            title = title_font.render("UNDER CONSTRUCTION", True, (255, 255, 255))
            prompt = message_font.render("Click anywhere or press Esc to return", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(MENU_SIZE[0] // 2, MENU_SIZE[1] // 2 - 20)))
            screen.blit(prompt, prompt.get_rect(center=(MENU_SIZE[0] // 2, MENU_SIZE[1] // 2 + 35)))
        else:
            screen.blit(bg, (0, 0))
            for name, image, rect in buttons:
                screen.blit(image, rect)

        #screen.blit()
        window_w, window_h = window.get_size()
        scale = min(window_w / MENU_SIZE[0], window_h / MENU_SIZE[1])
        render_size = (int(MENU_SIZE[0] * scale), int(MENU_SIZE[1] * scale))
        scaled_screen = pygame.transform.scale(screen, render_size)
        window.fill((12, 14, 24))
        window.blit(scaled_screen, ((window_w - render_size[0]) // 2, (window_h - render_size[1]) // 2))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

if __name__=="__main__":
    asyncio.run(main())
