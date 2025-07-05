import pygame
import sys
import random
import json
import os

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Refleks Oyunu")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
GREEN = (0, 255, 0)
COLORS = [
    GREEN,
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 255),
    (255, 0, 255),
]

COLOR_CHANGE_INTERVAL = 3000  # milliseconds
GAME_DURATION = 5 * 60 * 1000  # default game duration in milliseconds
LEADERBOARD_FILE = "leaderboard.json"


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)


def choose_new_color(current_color, allow_green=True):
    choices = [c for c in COLORS if c != current_color]
    if not allow_green:
        choices = [c for c in choices if c != GREEN]
    return random.choice(choices)


def draw_text(text, pos, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)
    return rect


def draw_button(text, pos):
    """Draw a button that highlights on hover."""
    rect = font.render(text, True, (0, 0, 0)).get_rect(center=pos)
    mouse_over = rect.collidepoint(pygame.mouse.get_pos())
    color = (255, 255, 0) if mouse_over else (255, 255, 255)
    return draw_text(text, pos, color)


def select_duration():
    """Allow the player to choose how long the game will last."""
    options = [
        (30, "30 Saniye"),
        (60, "1 Dakika"),
        (120, "2 Dakika"),
        (300, "5 Dakika"),
    ]
    while True:
        screen.fill((0, 0, 0))
        option_rects = []
        for i, (_, label) in enumerate(options):
            pos = (WIDTH // 2, HEIGHT // 2 - 90 + i * 60)
            rect = draw_button(label, pos)
            option_rects.append(rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for (secs, _), rect in zip(options, option_rects):
                    if rect.collidepoint(event.pos):
                        return secs * 1000
        clock.tick(60)


def show_leaderboard():
    data = load_leaderboard()
    while True:
        screen.fill((0, 0, 0))
        draw_text("Leaderboard", (WIDTH // 2, 40))
        y = 100
        for i, entry in enumerate(data, start=1):
            line = f"{i}. Avg: {entry['average']:.2f} ms Times: {entry['times']}"
            draw_text(line, (WIDTH // 2, y))
            y += 40
        back_rect = draw_button("Geri", (WIDTH // 2, HEIGHT - 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
        clock.tick(60)


def main_menu():
    while True:
        screen.fill((0, 0, 0))
        start_rect = draw_button("Başla", (WIDTH // 2, HEIGHT // 2 - 60))
        leaderboard_rect = draw_button("Leaderboard", (WIDTH // 2, HEIGHT // 2))
        exit_rect = draw_button("Kapat", (WIDTH // 2, HEIGHT // 2 + 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    duration = select_duration()
                    run_game(duration)
                if leaderboard_rect.collidepoint(event.pos):
                    show_leaderboard()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        clock.tick(60)


def run_game(duration_ms):
    current_color = random.choice(COLORS)
    last_change = pygame.time.get_ticks()
    waiting_for_press = False
    green_time = 0
    if current_color == GREEN:
        green_time = pygame.time.get_ticks()
        waiting_for_press = True
    responses = []

    start_time = pygame.time.get_ticks()
    end_time = start_time + duration_ms

    exit_rect = pygame.Rect(0, 0, 0, 0)
    while pygame.time.get_ticks() < end_time:
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, current_color, (WIDTH // 2, HEIGHT // 2), 75)
        exit_rect = draw_button("Kapat", (WIDTH - 60, 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and waiting_for_press:
                    responses.append(pygame.time.get_ticks() - green_time)
                    waiting_for_press = False
                    now = pygame.time.get_ticks()
                    # immediately change to a non-green color
                    current_color = choose_new_color(current_color, allow_green=False)
                    last_change = now
            
        now = pygame.time.get_ticks()
        if now - last_change >= COLOR_CHANGE_INTERVAL:
            current_color = choose_new_color(current_color)
            last_change = now
            if current_color == GREEN:
                green_time = now
                waiting_for_press = True
            else:
                waiting_for_press = False

        clock.tick(60)

    # Save results to leaderboard
    avg = sum(responses) / len(responses) if responses else 0
    data = load_leaderboard()
    data.append({"average": avg, "times": responses})
    save_leaderboard(data)


def main():
    main_menu()


if __name__ == "__main__":
    main()
