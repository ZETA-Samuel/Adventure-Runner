import asyncio
import os
import pygame


async def run_game():
    pygame.init()
    size = width, height = 640, 640
    display = pygame.display.Info()
    desktop_w = display.current_w or 900
    desktop_h = display.current_h or 900
    window = pygame.display.set_mode((min(1000, desktop_w), min(900, desktop_h)), pygame.RESIZABLE)
    screen = pygame.Surface(size)
    pygame.display.set_caption("Climb")
    clock = pygame.time.Clock()
    base = os.path.dirname(__file__)

    def image(path):
        return pygame.image.load(os.path.join(base, path)).convert_alpha()

    background = pygame.transform.scale(
        pygame.image.load(os.path.join(base, "images/Background/Gray.png")).convert(), size
    )
    grass = pygame.transform.scale(image("images/Terrain/grass.png"), (32, 32))
    brick = pygame.transform.scale(image("images/Terrain/brick.png"), (32, 32))
    spike = pygame.transform.scale(image("images/Traps/Spikes/Idle.png"), (32, 32))
    idle = pygame.transform.scale(image("images/Main Characters/Mask Dude/Jump (32x32).png"), (26, 26))
    exit_gate = pygame.transform.scale(image("images/Items/Checkpoints/End/End (Idle).png"), (64, 64))

    tile = 32
    platforms = []
    hazards = []
    ledges = [
        (16, 0, 20), (14, 6, 20), (12, 0, 13), (10, 7, 20),
        (8, 0, 12), (6, 7, 20), (4, 0, 13), (2, 7, 20),
    ]
    for row, start, end in ledges:
        for col in range(start, end):
            if row == 16 and col == 1:
                continue
            rect = pygame.Rect(col * tile, row * tile, tile, tile)
            platforms.append((rect, brick))
    for row, col in [(11, 4), (7, 15)]:
        hazards.append(pygame.Rect(col * tile, row * tile, tile, tile))
    # A solid starting floor and a finish platform at the top.
    for col in range(width // tile):
        platforms.append((pygame.Rect(col * tile, height - tile, tile, tile), grass))

    player = pygame.Rect(48, 550, 22, 27)
    spawn = player.topleft
    finish = pygame.Rect(width - 88, 0, 64, 64)
    velocity_y = 0.0
    gravity = 1200.0
    jump_speed = -650.0
    move_speed = 240.0
    grounded = False
    jump_buffer = 0.0
    coyote_time = 0.0
    camera_y = 0
    won = False
    font = pygame.font.Font(os.path.join(base, "images/fonts/PixelOperator8-Bold.ttf"), 28)
    small_font = pygame.font.Font(os.path.join(base, "images/fonts/PixelOperator8.ttf"), 16)

    def restart():
        nonlocal velocity_y, grounded, won, jump_buffer, coyote_time
        player.topleft = spawn
        velocity_y = 0
        grounded = False
        jump_buffer = 0
        coyote_time = 0
        won = False

    running = True
    while running:
        dt = min(clock.tick(60) / 1000, 0.04)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    jump_buffer = 0.14
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif won and event.key == pygame.K_r:
                    restart()

        keys = pygame.key.get_pressed()
        if not won:
            jump_buffer = max(0, jump_buffer - dt)
            coyote_time = 0.12 if grounded else max(0, coyote_time - dt)
            dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
            player.x += int(dx * move_speed * dt)
            player.x = max(0, min(width - player.width, player.x))
            for rect, _ in platforms:
                if player.colliderect(rect):
                    if dx > 0:
                        player.right = rect.left
                    elif dx < 0:
                        player.left = rect.right

            if jump_buffer > 0 and coyote_time > 0:
                velocity_y = jump_speed
                grounded = False
                coyote_time = 0
                jump_buffer = 0
            velocity_y = min(velocity_y + gravity * dt, 850)
            previous_bottom = player.bottom
            player.y += int(velocity_y * dt)
            grounded = False
            for rect, _ in platforms:
                if player.colliderect(rect):
                    if velocity_y >= 0 and previous_bottom <= rect.top:
                        player.bottom = rect.top
                        grounded = True
                    elif velocity_y < 0:
                        player.top = rect.bottom
                    else:
                        continue
                    velocity_y = 0

            if player.top < 0:
                player.top = 0
                velocity_y = 0

            if any(player.colliderect(rect) for rect in hazards) or player.top > height + 30:
                restart()
            if player.colliderect(finish):
                won = True

        camera_y = 0
        screen.blit(background, (0, 0))
        for rect, texture in platforms:
            screen.blit(texture, (rect.x, rect.y - camera_y))
        for rect in hazards:
            screen.blit(spike, (rect.x, rect.y - camera_y))
        screen.blit(exit_gate, (finish.x, finish.y - camera_y))
        screen.blit(idle, (player.centerx - idle.get_width() // 2, player.y - camera_y))

        if won:
            shade = pygame.Surface(size, pygame.SRCALPHA)
            shade.fill((10, 15, 30, 190))
            screen.blit(shade, (0, 0))
            title = font.render("YOU MADE IT!", True, (255, 231, 120))
            prompt = small_font.render("Press R to climb again  |  Esc to quit", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(width // 2, height // 2 - 20)))
            screen.blit(prompt, prompt.get_rect(center=(width // 2, height // 2 + 25)))
        window_w, window_h = window.get_size()
        scale = min(window_w / width, window_h / height)
        render_size = (int(width * scale), int(height * scale))
        scaled = pygame.transform.scale(screen, render_size)
        window.fill((12, 14, 24))
        window.blit(scaled, ((window_w - render_size[0]) // 2, (window_h - render_size[1]) // 2))
        pygame.display.flip()
        await asyncio.sleep(0)
