import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 990, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stick Hero")
clock = pygame.time.Clock()

ZOOM = 0.5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (200, 30, 30)

# Scaled constants
TARGET_PLATFORM_HEIGHT = int(590 * ZOOM)
PLATFORM_Y = HEIGHT - TARGET_PLATFORM_HEIGHT
hero_width = int(50 * ZOOM)
hero_height = int(50 * ZOOM)

# Load and scale background
bg_raw = pygame.image.load("background1.png").convert()
bg = pygame.transform.smoothscale(bg_raw, (WIDTH, HEIGHT))

# Load and scale hero
hero_img = pygame.image.load("hero.png")
hero_img = pygame.transform.scale(hero_img, (hero_width, hero_height))

# Function to load and scale platform
def scale_platform(image_path, width):
    img = pygame.image.load(image_path)
    scaled_width = int(width * ZOOM)
    scaled_height = TARGET_PLATFORM_HEIGHT
    return pygame.transform.scale(img, (scaled_width, scaled_height)), scaled_width

# Platform pool
platform_pool = [
    scale_platform("platform.png", 40),
    scale_platform("platform1.png", 60),
    scale_platform("platform1.png", 90),
    scale_platform("platform1.png", 130),
    scale_platform("platform1.png", 30)
]

# Game variables
platforms = []
platform_spacing = int(150 * ZOOM)
x_cursor = 100
for _ in range(8):
    img, w = random.choice(platform_pool)
    platforms.append([x_cursor, PLATFORM_Y, img, w])
    x_cursor += w + platform_spacing

hero_x = platforms[0][0] + platforms[0][3] - hero_width
hero_y = PLATFORM_Y - hero_height

stick_len = 0
stick_growing = False
stick_angle = 0
rotating = False
hero_moving = False
scrolling = False
scroll_speed = int(6 * ZOOM)
scroll_offset = 0
scroll_target = 0

stick_x = 0
stick_y = 0

score = 0
game_over = False
falling = False
fall_speed = int(7 * ZOOM)

landing_platform = None

font = pygame.font.SysFont("arial", int(48 * ZOOM), bold=True)
small_font = pygame.font.SysFont("arial", int(36 * ZOOM))

show_instruction = True

def draw_platforms():
    for p in platforms:
        screen.blit(p[2], (p[0] - scroll_offset, HEIGHT - TARGET_PLATFORM_HEIGHT))

def draw_stick():
    if stick_len > 0:
        x0 = stick_x - scroll_offset
        y0 = stick_y
        x1 = x0 + stick_len * math.sin(math.radians(stick_angle))
        y1 = y0 - stick_len * math.cos(math.radians(stick_angle))
        pygame.draw.line(screen, BLACK, (x0, y0), (x1, y1), max(2, int(5 * ZOOM)))

def draw_hero():
    screen.blit(hero_img, (hero_x - scroll_offset, hero_y))

def draw_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (20, 20))

def draw_instruction():
    if show_instruction:
        instruction_font = pygame.font.SysFont("arial", int(35 * ZOOM))
        line1 = instruction_font.render("Hold down the mouse to", True, BLACK)
        line2 = instruction_font.render("stretch out a stick", True, BLACK)
        x = WIDTH // 2
        y = HEIGHT // 2 - 80
        screen.blit(line1, (x - line1.get_width() // 2, y))
        screen.blit(line2, (x - line2.get_width() // 2, y + line1.get_height() + 5))
def show_game_over_screen():
    center = (WIDTH // 2, HEIGHT // 2 - 30)
    radius = int(160 * ZOOM)
    pygame.draw.circle(screen, RED, center, radius)
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = small_font.render("Press ENTER to restart", True, WHITE)
    screen.blit(game_over_text, (
        center[0] - game_over_text.get_width() // 2,
        center[1] - game_over_text.get_height() // 2 - 10
    ))
    screen.blit(restart_text, (
        center[0] - restart_text.get_width() // 2,
        center[1] + 5
    ))
def generate_next_platform():
    last_x = platforms[-1][0] + platforms[-1][3]
    img, w = random.choice(platform_pool)
    return [last_x + random.randint(int(150 * ZOOM), int(250 * ZOOM)), PLATFORM_Y, img, w]
def restart_game():
    global platforms, x_cursor, hero_x, hero_y, stick_len, stick_growing, game_over
    global score, stick_angle, rotating, hero_moving, stick_x, stick_y, scroll_offset, falling
    global show_instruction, landing_platform
    platforms = []
    x_cursor = 100
    for _ in range(5):
        img, w = random.choice(platform_pool)
        platforms.append([x_cursor, PLATFORM_Y, img, w])
        x_cursor += w + platform_spacing
    hero_x = platforms[0][0] + platforms[0][3] - hero_width
    hero_y = PLATFORM_Y - hero_height
    stick_len = 0
    stick_growing = False
    stick_angle = 0
    rotating = False
    hero_moving = False
    scroll_offset = 0
    stick_x = 0
    stick_y = 0
    score = 0
    game_over = False
    falling = False
    show_instruction = True
    landing_platform = None

running = True
while running:
    screen.fill(WHITE)
    screen.blit(bg, (0, 0))
    draw_platforms()
    draw_stick()
    draw_hero()
    draw_score()
    draw_instruction()

    if game_over:
        show_game_over_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not rotating and not hero_moving and not falling and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                stick_growing = True
                show_instruction = False
            if event.type == pygame.MOUSEBUTTONUP:
                stick_growing = False
                rotating = True
                stick_x = hero_x + hero_width
                stick_y = hero_y + hero_height

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            restart_game()

    if stick_growing:
        stick_len += int(5 * ZOOM)
        stick_x = hero_x + hero_width
        stick_y = hero_y + hero_height

    if rotating:
        stick_angle += 5
        if stick_angle >= 90:
            stick_angle = 90
            rotating = False
            hero_moving = True

    if hero_moving:
        if hero_x + hero_width // 2 + 5 < stick_x + stick_len:
            hero_x += int(5 * ZOOM)
        else:
            hero_x = stick_x + stick_len - hero_width // 2


            tip_x = stick_x + stick_len
            landing_platform = None
            for p in platforms:
                if p[0] <= tip_x <= p[0] + p[3]:
                    landing_platform = p
                    break

            if landing_platform:
                scroll_target = landing_platform[0] - 100
                hero_moving = False
                scrolling = True
            else:
                falling = True
                hero_moving = False

    if falling:
        stick_angle += 5
        if stick_angle > 180:
            stick_angle = 180
        hero_y += fall_speed
        if hero_y > HEIGHT:
            falling = False
            game_over = True

    if scrolling and landing_platform:
        scroll_offset += scroll_speed
        if scroll_offset >= scroll_target:
            delta = scroll_target
            scroll_offset = 0

            for p in platforms:
                p[0] -= delta
            hero_x -= delta

            scrolling = False
            hero_x = landing_platform[0] + landing_platform[3] - hero_width
            platforms.append(generate_next_platform())

            stick_len = 0
            stick_angle = 0
            stick_x = 0
            stick_y = 0
            score += 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()