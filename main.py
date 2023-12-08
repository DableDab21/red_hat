import pygame
import sys
import os
import random

def load_and_scale_image(image_path, size):
    image = pygame.image.load(os.path.join("Images", image_path)).convert_alpha()
    return pygame.transform.scale(image, size)

def create_panches():
    return [(panch_image.get_rect(center=(random.randint(100, width - 100), -100)), speed) for speed in panch_speeds]

pygame.init()

width, height = 960, 960
screen = pygame.display.set_mode((width, height))

background_image_path = os.path.join("Images", "background.png")
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (width, height))
else:
    print(f"File not found: {background_image_path}")
    pygame.quit()
    sys.exit()

pygame.display.set_caption("Персонаж в окне")

character_size = 128
new_character_size = (45, 90)

character_image = load_and_scale_image("red_hat.png", new_character_size)
character_rect = character_image.get_rect(center=(100, 880))

volf_image = load_and_scale_image("volf.png", (character_size, character_size))
volf_rect = volf_image.get_rect(center=(-100, -100))

table_image = load_and_scale_image("table.png", (character_size, character_size))
table_rect = table_image.get_rect(center=(850, 880))

panch_image = load_and_scale_image("panch.png", (character_size, character_size))
panch_speeds = [1, 1, 1]
panches = create_panches()

character_speed = 5

clock = pygame.time.Clock()
new_font_size = 72
text_color = (0, 0, 0)  # белый

font = pygame.font.Font(None, new_font_size)

meet_event_triggered = False
win_timer_started = False
win_timer_duration = 30
falling_panches = False
game_over_timer_started = False
game_over_timer_duration = 1000  # 1 секунда
game_won = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for panch_rect, _ in panches:
        if character_rect.colliderect(panch_rect) and not game_over_timer_started:
            falling_panches = False
            if win_timer_started:
                character_dialogue = ["Вы проиграли!"]
                game_over_timer_started = True
                game_over_timer_start_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if not game_over_timer_started:
        character_rect.x += (keys[pygame.K_d] - keys[pygame.K_a]) * character_speed
        character_rect.x = max(0, min(character_rect.x, width - character_size))

    if character_rect.colliderect(volf_rect) and not meet_event_triggered:
        meet_event_triggered = True
        volf_rect.center = (-100, -100)
        table_rect.center = (-100, -100)
        background_image_path = os.path.join("Images", "background3.png")
        if os.path.exists(background_image_path):
            background_image = pygame.image.load(background_image_path).convert()
            background_image = pygame.transform.scale(background_image, (width, height))
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            win_timer_started = True
            win_timer_start_time = pygame.time.get_ticks()
            falling_panches = True
        else:
            print(f"File not found: {background_image_path}")
            pygame.quit()
            sys.exit()
        character_rect.center = (450, 880)

    if character_rect.colliderect(table_rect):
        background_image_path = os.path.join("Images", "background2.png")
        if os.path.exists(background_image_path):
            background_image = pygame.image.load(background_image_path).convert()
            background_image = pygame.transform.scale(background_image, (width, height))
            table_rect.center = (-100, -100)
            volf_rect.center = (850, 880)
            panches = create_panches()
        else:
            print(f"File not found: {background_image_path}")
            pygame.quit()
            sys.exit()
        character_rect.center = (100, 880)

    if win_timer_started:
        elapsed_time = pygame.time.get_ticks() - win_timer_start_time
        remaining_time = max(0, win_timer_duration * 1000 - elapsed_time)
        seconds = remaining_time // 1000
        timer_text = font.render(f"Time: {seconds} seconds", True, (0, 0, 0))
        screen.blit(timer_text, (width - 200, 20))

        if elapsed_time >= win_timer_duration * 1000:
            win_timer_started = False
            game_won = True
            game_over_timer_started = True
            game_over_timer_start_time = pygame.time.get_ticks()

    if falling_panches:
        for i, (panch_rect, panch_speed) in enumerate(panches):
            panch_rect.y += panch_speed
            if panch_rect.y > height:
                panch_rect.y = -100
                new_x = random.randint(0, width - character_size)
                while any(abs(new_x - rect.x) < 50 for rect, _ in panches):
                    new_x = random.randint(0, width - character_size)
                panch_rect.x = new_x
                panches[i] = (panch_rect, panch_speed)

    screen.blit(background_image, (0, 0))
    screen.blit(character_image, character_rect.topleft)
    screen.blit(volf_image, volf_rect.topleft)
    screen.blit(table_image, table_rect.topleft)

    for panch_rect, _ in panches:
        screen.blit(panch_image, panch_rect.topleft)

    if game_over_timer_started:
        elapsed_time = pygame.time.get_ticks() - game_over_timer_start_time
        if elapsed_time >= game_over_timer_duration:
            if game_won:
                character_dialogue = ["Вы выиграли!"]
            game_over_surface = font.render(character_dialogue[0], True, text_color)
            game_over_rect = game_over_surface.get_rect(center=(width // 2, height // 2 - 300))
            screen.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            pygame.time.delay(1000)  # Подождать 1 секунду
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)