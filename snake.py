import pygame
import sys
import random
import time
import numpy as np
import os
import json

check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Pygame başlatılırken {check_errors[1]} hata bulundu, çıkılıyor...')
    sys.exit(-1)
else:
    print('[+] Pygame başarıyla başlatıldı.')

pygame.mixer.init(44100, -16, 2, 2048)

screen_width = 1080
screen_height = 720
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Aşırı Basit Yılan Oyunu')

try:
    game_icon = pygame.image.load('yilan.ico')
    pygame.display.set_icon(game_icon)
    print('[+] Oyun simgesi başarıyla yüklendi.')
except pygame.error as e:
    print(f"[-] Oyun simgesi yüklenirken bir Pygame hatası oluştu: {e}. Varsayılan simge kullanılacak.")

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
ORANGE = pygame.Color(255, 165, 0)
PURPLE = pygame.Color(128, 0, 128)
YELLOW = pygame.Color(255, 255, 0)
CYAN = pygame.Color(0, 255, 255)
MAGENTA = pygame.Color(255, 0, 255)
PINK = pygame.Color(255, 192, 203)
BROWN = pygame.Color(165, 42, 42)
LIME_GREEN = pygame.Color(50, 205, 50)
TEAL = pygame.Color(0, 128, 128)
GOLD = pygame.Color(255, 215, 0)

GAME_COLORS = [WHITE, RED, BLUE, ORANGE, PURPLE, YELLOW, CYAN, MAGENTA, PINK, BROWN, LIME_GREEN, TEAL, GOLD]

fps_controller = pygame.time.Clock()
BLOCK_SIZE = 10

frequency = 800
duration = 0.05
sample_rate = pygame.mixer.get_init()[0]
num_samples = int(sample_rate * duration)
mono_wave = np.array([4096 * np.sin(2.0 * np.pi * frequency * x / sample_rate) for x in range(num_samples)]).astype(np.int16)
arr = np.column_stack((mono_wave, mono_wave))
beep_sound = pygame.sndarray.make_sound(arr)

SCORES_FILE = "scores.json"

def save_score(score, name):
    scores = load_scores()
    if isinstance(scores, list) and all(isinstance(item, int) for item in scores):
        scores = [{"name": "---", "score": s} for s in scores]
    scores.append({"name": name.upper(), "score": score})
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def reset_scores():
    with open(SCORES_FILE, 'w') as f:
        json.dump([], f)

def get_player_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) == 3:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 3 and event.unicode.isalpha():
                    name += event.unicode.upper()

        game_window.fill(BLACK)
        font = pygame.font.SysFont('comicsansms', 40)
        text = font.render("3 Harf Gir (ENTER ile kaydet): " + name, True, WHITE)
        rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        game_window.blit(text, rect)
        pygame.display.flip()
    return name

def show_top_scores():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    start_screen()
                if reset_button_rect.collidepoint(pygame.mouse.get_pos()):
                    reset_scores()

        game_window.fill(BLACK)
        title_font = pygame.font.SysFont('comicsansms', 50)
        title_text = title_font.render('En İyi 5 Skor', True, YELLOW)
        title_rect = title_text.get_rect(center=(screen_width / 2, 72))
        game_window.blit(title_text, title_rect)

        scores = load_scores()
        score_font = pygame.font.SysFont('consolas', 30)
        for i, entry in enumerate(scores):
            line = score_font.render(f"{i+1}. {entry['name']} - {entry['score']} Puan", True, WHITE)
            game_window.blit(line, (screen_width/2 - 150, 150 + i * 40))

        back_button_rect = draw_button("Ana Menü", (screen_width / 2) - 210, screen_height - 100, 200, 50, RED, GREEN, start_screen)
        reset_button_rect = draw_button("Skorları Sıfırla", (screen_width / 2) + 10, screen_height - 100, 240, 50, RED, GREEN, reset_scores)

        pygame.display.update()
        fps_controller.tick(30)

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Skor : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (screen_width / 10, 15)
    else:
        score_rect.midtop = (screen_width / 2, screen_height / 1.25)
    game_window.blit(score_surface, score_rect)

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_window, active_color, (x, y, width, height), border_radius=5)
        if click[0] == 1 and action is not None:
            pygame.time.delay(200)
            action()
    else:
        pygame.draw.rect(game_window, inactive_color, (x, y, width, height), border_radius=5)

    small_text = pygame.font.SysFont('comicsansms', 28)
    text_surf = small_text.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    game_window.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

def start_screen():
    global score
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_window.fill(BLACK)

        large_text = pygame.font.SysFont('comicsansms', 60)
        text_surf = large_text.render('Aşırı Basit Yılan Oyunu', True, GREEN)
        text_rect = text_surf.get_rect()
        text_rect.center = ((screen_width / 2), (screen_height / 4))
        game_window.blit(text_surf, text_rect)

        draw_button("Oyunu Başlat", (screen_width / 2) - 100, (screen_height / 2) + 50, 200, 50, CYAN, RED, main)
        draw_button("Skor Tablosu", (screen_width / 2) - 100, (screen_height / 2) + 120, 200, 50, CYAN, RED, show_top_scores)

        pygame.display.update()
        fps_controller.tick(30)

def game_over():
    name = get_player_name()
    save_score(score, name)
    my_font = pygame.font.SysFont('comicsansms', 80)
    game_over_surface = my_font.render('Oyun Bitti', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, RED, 'times', 20)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button_rect.collidepoint(mouse_pos):
                    main()
                if main_menu_button_rect.collidepoint(mouse_pos):
                    start_screen()

        restart_button_rect = draw_button("Yeniden Başlat", (screen_width / 2) - 100, (screen_height / 2) + 20, 200, 50, GREEN, RED, None)
        main_menu_button_rect = draw_button("Ana Menü", (screen_width / 2) - 100, (screen_height / 2) + 90, 200, 50, RED, GREEN, None)

        pygame.display.update()
        fps_controller.tick(30)

def main():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score, speed, food_color, snake_color

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]

    food_pos = [random.randrange(1, (screen_width // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(1, (screen_height // BLOCK_SIZE)) * BLOCK_SIZE]
    food_spawn = True

    food_color = random.choice(GAME_COLORS)
    snake_color = random.choice(GAME_COLORS)

    direction = 'RIGHT'
    change_to = direction

    score = 0
    speed = 15

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            speed += 0.5
            food_spawn = False
            food_color = random.choice(GAME_COLORS)
            snake_color = random.choice(GAME_COLORS)
            beep_sound.play()
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (screen_width // BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(1, (screen_height // BLOCK_SIZE)) * BLOCK_SIZE]
        food_spawn = True

        game_window.fill(BLACK)

        for pos in snake_body:
            pygame.draw.rect(game_window, snake_color, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(game_window, food_color, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        if snake_pos[0] < 0 or snake_pos[0] > screen_width - BLOCK_SIZE or snake_pos[1] < 0 or snake_pos[1] > screen_height - BLOCK_SIZE:
            game_over()

        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        show_score(1, WHITE, 'consolas', 20)
        pygame.display.update()
        fps_controller.tick(speed)

if __name__ == '__main__':
    start_screen()