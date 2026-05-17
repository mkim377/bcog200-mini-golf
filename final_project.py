import pygame
import sys
import math

pygame.init()

background_color = (79, 121, 66)
# Colors
dark_green = (43, 92, 34)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 100, 255)
brown = (150, 75, 0)
# Screen
width, height = (1000, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mini_Golf_Game")

# Fonts
title_font = pygame.font.SysFont("arial", 75)
button_font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 30)

play_button = pygame.Rect(400, 375, 200, 80)
quit_button = pygame.Rect(400, 475, 200, 80)

MENU = "menu"
CONTROLS = "controls"
GAME = "game"
WIN = "win"

state = MENU
clock = pygame.time.Clock()

ball_radius = 15
ball_speed_x = 0
ball_speed_y = 0
ball_moving = False

angle = 0
power = 0
charging = False

strokes = 0

hole_scores = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
}

current_hole = 1

pars = {
    1: 2,
    2: 3,
    3: 5,
    4: 3,
    5: 5,
    6: 6,
    7: 5,
    8: 5,
    9: 6,
}


hole_layout = {
    1: {
        "ball_start": (150, 400),
        "hole_pos": (850, 400),
        "walls": [],
        "water": [],
    },
    2: {
        "ball_start": (120, 700),
        "hole_pos": (900, 100),
        "walls": [
            pygame.Rect(350, 200, 30, 400),
            pygame.Rect(650, 0, 30, 450),
        ],
        "water": [],
    },
    3: {
        "ball_start": (100, 700),
        "hole_pos": (900, 120),
        "walls": [
            pygame.Rect(300, 0, 30, 500),
            pygame.Rect(550, 250, 30, 550),
            pygame.Rect(780, 0, 30, 350),
        ],
        "water": [
            pygame.Rect(520, 120, 140, 70),
        ],
    },
    4: {
        "ball_start": (120, 650),
        "hole_pos": (900, 120),
        "walls": [
            pygame.Rect(250, 0, 30, 500),
            pygame.Rect(500, 300, 30, 500),
            pygame.Rect(750, 0, 30, 450),
        ],
        "water": [
            pygame.Rect(380, 620, 110, 45),
        ],
    },
    5: {
        "ball_start": (120, 700),
        "hole_pos": (900, 100),
        "walls": [
            pygame.Rect(180, 0, 30, 600),
            pygame.Rect(400, 200, 30, 600),
            pygame.Rect(620, 0, 30, 500),
        ],
        "water": [
            pygame.Rect(280, 650, 100, 40),
            pygame.Rect(520, 320, 110, 40),
        ],
    },
    6: {  # OLD HOLE 5
        "ball_start": (100, 720),
        "hole_pos": (920, 100),
        "walls": [
            pygame.Rect(220, 150, 30, 650),
            pygame.Rect(420, 0, 30, 500),
            pygame.Rect(620, 250, 30, 550),
            pygame.Rect(820, 0, 30, 400),
        ],
        "water": [
            pygame.Rect(500, 580, 120, 45),
            pygame.Rect(720, 180, 100, 40),
        ],
    },
    7: {
        "ball_start": (100, 740),
        "hole_pos": (920, 90),
        "walls": [
            pygame.Rect(200, 0, 30, 600),
            pygame.Rect(400, 200, 30, 600),
            pygame.Rect(620, 0, 30, 500),
            pygame.Rect(820, 250, 30, 450),
        ],
        "water": [
            pygame.Rect(300, 680, 100, 40),
            pygame.Rect(540, 420, 100, 40),
            pygame.Rect(720, 120, 100, 40),
        ],
    },
    8: {
        "ball_start": (100, 720),
        "hole_pos": (920, 100),
        "walls": [
            pygame.Rect(180, 150, 30, 650),
            pygame.Rect(420, 0, 30, 500),
            pygame.Rect(650, 250, 30, 550),
        ],
        "water": [
            pygame.Rect(250, 650, 100, 40),
            pygame.Rect(520, 120, 100, 40),
        ],
    },
    9: {
        "ball_start": (100, 740),
        "hole_pos": (920, 90),
        "walls": [
            pygame.Rect(180, 100, 30, 700),
            pygame.Rect(350, 0, 30, 500),
            pygame.Rect(520, 250, 30, 550),
            pygame.Rect(700, 0, 30, 500),
            pygame.Rect(860, 250, 30, 400),
        ],
        "water": [
            pygame.Rect(250, 680, 100, 40),
            pygame.Rect(450, 500, 100, 40),
            pygame.Rect(650, 120, 100, 40),
        ],
    },
}

ball_x, ball_y = hole_layout[current_hole]["ball_start"]

hole_x, hole_y = hole_layout[current_hole]["hole_pos"]
hole_radius = 20


def load_hole(hole_number):

    global ball_x
    global ball_y
    global hole_x
    global hole_y
    global ball_speed_x
    global ball_speed_y
    global ball_moving
    global angle
    global power

    ball_x, ball_y = hole_layout[hole_number]["ball_start"]

    hole_x, hole_y = hole_layout[hole_number]["hole_pos"]

    ball_speed_x = 0
    ball_speed_y = 0

    ball_moving = False

    angle = 0
    power = 0


# Checkerboard Background


def draw_checkerboard(tile_size=50):

    for row in range(0, height, tile_size):
        for col in range(0, width, tile_size):

            if (row // tile_size + col // tile_size) % 2 == 0:
                color = background_color
            else:
                color = dark_green

            pygame.draw.rect(screen, color, (col, row, tile_size, tile_size))


# Menu Screen


def draw_menu():

    draw_checkerboard()

    title_text = title_font.render("Mini Golf by Martin Kim", True, white)

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 225))

    pygame.draw.rect(screen, (0, 255, 0), play_button)

    play_text = button_font.render("PLAY", True, black)

    screen.blit(play_text, (play_button.x + 50, play_button.y + 20))

    pygame.draw.rect(screen, (255, 0, 0), quit_button)

    quit_text = button_font.render("QUIT", True, black)

    screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 20))


# Controls


def controls_page():

    draw_checkerboard()

    title = title_font.render("Controls", True, white)
    screen.blit(title, (width // 2 - title.get_width() // 2, 200))

    text_1 = button_font.render("Use LEFT and RIGHT arrows to aim", True, white)

    screen.blit(text_1, (width // 2 - text_1.get_width() // 2, 300))

    text_2 = button_font.render("Hold SPACE to gain power", True, white)

    screen.blit(text_2, (width // 2 - text_2.get_width() // 2, 400))

    text_3 = button_font.render("Release SPACE to shoot", True, white)

    screen.blit(text_3, (width // 2 - text_3.get_width() // 2, 500))

    text_4 = button_font.render("Press ENTER to continue", True, white)

    screen.blit(text_4, (width // 2 - text_4.get_width() // 2, 600))


# Game screen


def draw_game():

    draw_checkerboard()

    # Draw hole
    pygame.draw.circle(screen, black, (hole_x, hole_y), hole_radius)

    # Draw walls
    for wall in hole_layout[current_hole]["walls"]:
        pygame.draw.rect(screen, brown, wall)

    # Draw water
    for water in hole_layout[current_hole]["water"]:
        pygame.draw.rect(screen, blue, water)

    # Draw ball
    pygame.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_radius)

    # Aim line
    if not ball_moving:

        line_length = 100

        end_x = ball_x + math.cos(math.radians(angle)) * line_length
        end_y = ball_y - math.sin(math.radians(angle)) * line_length

        pygame.draw.line(screen, white, (ball_x, ball_y), (end_x, end_y), 5)

    # Power bar
    pygame.draw.rect(screen, white, (50, 50, power * 4, 30))

    power_text = small_font.render("Power", True, white)
    screen.blit(power_text, (50, 10))

    # Total strokes
    stroke_text = small_font.render("Total Strokes: " + str(strokes), True, white)

    screen.blit(stroke_text, (700, 20))

    # Current hole score
    current_score_text = small_font.render(
        "Hole Score: " + str(hole_scores[current_hole]), True, white
    )

    screen.blit(current_score_text, (700, 60))

    # Hole number
    hole_text = small_font.render("Hole " + str(current_hole), True, white)

    screen.blit(hole_text, (50, 120))

    # Par
    par_text = small_font.render("Par " + str(pars[current_hole]), True, white)

    screen.blit(par_text, (50, 160))


# Ball movement


def move_ball():

    global ball_x
    global ball_y
    global ball_speed_x
    global ball_speed_y
    global ball_moving
    global current_hole
    global state
    global strokes

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Friction
    ball_speed_x *= 0.99
    ball_speed_y *= 0.99

    # Stop ball
    if abs(ball_speed_x) < 0.1 and abs(ball_speed_y) < 0.1:

        ball_speed_x = 0
        ball_speed_y = 0

        ball_moving = False

    # Screen walls
    if ball_x <= ball_radius or ball_x >= width - ball_radius:
        ball_speed_x *= -1

    if ball_y <= ball_radius or ball_y >= height - ball_radius:
        ball_speed_y *= -1

    # Wall collisions
    ball_rect = pygame.Rect(
        ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2
    )

    for wall in hole_layout[current_hole]["walls"]:

        if ball_rect.colliderect(wall):

            # Bounce like screen borders
            if ball_rect.centerx < wall.left or ball_rect.centerx > wall.right:
                ball_speed_x *= -1

            if ball_rect.centery < wall.top or ball_rect.centery > wall.bottom:
                ball_speed_y *= -1

    # Water hazards
    for water in hole_layout[current_hole]["water"]:

        # Find closest point on water rectangle to center of ball
        closest_x = max(water.left, min(ball_x, water.right))
        closest_y = max(water.top, min(ball_y, water.bottom))

        # Distance from ball center to water
        distance_x = ball_x - closest_x
        distance_y = ball_y - closest_y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        # Only count as water if about 75% of the ball is touching
        if distance < ball_radius / 4:

            strokes += 1
            hole_scores[current_hole] += 1

            ball_x, ball_y = hole_layout[current_hole]["ball_start"]

            ball_speed_x = 0
            ball_speed_y = 0

            ball_moving = False

    # Hole detection
    distance = math.sqrt((ball_x - hole_x) ** 2 + (ball_y - hole_y) ** 2)

    if distance < hole_radius:

        current_hole += 1

        if current_hole > 9:
            state = WIN

        else:
            load_hole(current_hole)


# Win screen


def draw_win_screen():

    draw_checkerboard()

    win_text = title_font.render("Final Scorecard", True, white)

    screen.blit(win_text, (width // 2 - win_text.get_width() // 2, 65))

    # Scorecard box
    pygame.draw.rect(screen, white, (220, 140, 560, 600), 4)

    # Headers
    headers = ["Hole", "Par", "Score"]

    x_positions = [280, 480, 650]

    for i in range(len(headers)):

        header_text = button_font.render(headers[i], True, white)
        screen.blit(header_text, (x_positions[i], 190))

    # Hole rows
    for hole in range(1, 10):

        y = 230 + (hole - 1) * 40

        hole_text = small_font.render(str(hole), True, white)
        par_text = small_font.render(str(pars[hole]), True, white)
        score_text = small_font.render(str(hole_scores[hole]), True, white)

        screen.blit(hole_text, (300, y))
        screen.blit(par_text, (500, y))
        screen.blit(score_text, (680, y))

    # Totals
    total_par = sum(pars.values())

    total_par_text = small_font.render("Par: " + str(total_par), True, white)

    total_score_text = small_font.render("Score: " + str(strokes), True, white)

    screen.blit(total_par_text, (260, 760))
    screen.blit(total_score_text, (520, 760))

    quit_text = button_font.render("Press ESC to quit", True, white)

    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 650))


# Main loop

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Menu
        if state == MENU:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_button.collidepoint(event.pos):
                    state = CONTROLS

                if quit_button.collidepoint(event.pos):
                    running = False

        # Controls
        elif state == CONTROLS:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    state = GAME

        # Game
        elif state == GAME:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and not ball_moving:
                    charging = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE and not ball_moving:

                    charging = False
                    ball_moving = True

                    strokes += 1
                    hole_scores[current_hole] += 1

                    ball_speed_x = math.cos(math.radians(angle)) * (power / 2.5)
                    ball_speed_y = -math.sin(math.radians(angle)) * (power / 2.5)

                    power = 0

        # Win screen
        elif state == WIN:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

    # Game
    if state == GAME:

        keys = pygame.key.get_pressed()

        if not ball_moving:

            if keys[pygame.K_LEFT]:
                angle += 2

            if keys[pygame.K_RIGHT]:
                angle -= 2

        if charging:

            power += 1

            if power > 25:
                power = 25

        move_ball()

    # Drawing
    if state == MENU:
        draw_menu()

    elif state == CONTROLS:
        controls_page()

    elif state == GAME:
        draw_game()

    elif state == WIN:
        draw_win_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
