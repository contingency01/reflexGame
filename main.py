import pygame
import sys
import random

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reflex Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
GREEN = (0, 255, 0)
COLORS = [
    GREEN,
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
]

COLOR_CHANGE_INTERVAL = 4000  # milliseconds
GAME_DURATION = 5 * 60 * 1000  # default game duration in milliseconds


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
        (30, "30 Seconds"),
        (60, "1 Minute"),
        (120, "2 Minutes"),
        (300, "5 Minutes"),
    ]
    while True:
        option_rects = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for (secs, _), rect in zip(options, option_rects):
                    if rect.collidepoint(event.pos):
                        return secs * 1000

        screen.fill((0, 0, 0))
        for i, (_, label) in enumerate(options):
            pos = (WIDTH // 2, HEIGHT // 2 - 90 + i * 60)
            rect = draw_button(label, pos)
            option_rects.append(rect)
        pygame.display.flip()
        clock.tick(60)


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return select_duration()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        start_rect = draw_button("Start Game", (WIDTH // 2, HEIGHT // 2 - 50))
        exit_rect = draw_button("Exit", (WIDTH // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(60)


def run_game(duration_ms):
    current_color = random.choice(COLORS)
    last_change = pygame.time.get_ticks()
    waiting_for_press = False
    green_time = 0
    responses = []

    start_time = pygame.time.get_ticks()
    end_time = start_time + duration_ms

    exit_rect = None
    while pygame.time.get_ticks() < end_time:
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
                    non_green = [c for c in COLORS if c != GREEN]
                    current_color = random.choice(non_green)
                    last_change = now
            
        now = pygame.time.get_ticks()
        if now - last_change >= COLOR_CHANGE_INTERVAL:
            current_color = random.choice(COLORS)
            last_change = now
            if current_color == GREEN:
                green_time = now
                waiting_for_press = True
            else:
                waiting_for_press = False

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, current_color, (WIDTH // 2, HEIGHT // 2), 75)
        exit_rect = draw_button("Exit", (WIDTH - 60, 30))
        pygame.display.flip()
        clock.tick(60)

    # Calculate average reaction time
    if responses:
        avg = sum(responses) / len(responses)
        result_text = f"Average Reaction: {avg:.2f} ms"
    else:
        result_text = "No reactions recorded"

    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
        screen.fill((0, 0, 0))
        draw_text(result_text, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(60)


def main():
    while True:
        duration = main_menu()
        run_game(duration)


if __name__ == "__main__":
    main()
