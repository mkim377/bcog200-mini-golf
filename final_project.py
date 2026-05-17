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

hole_scores = {1: 0, 2: 0, 3: 0}

    screen.blit(text_1, (width // 2 - text_1.get_width() // 2, 300))

    text_2 = button_font.render("Hold SPACE to gain power", True, white)

pars = {1: 2, 2: 3, 3: 5}

ball_x = 150
ball_y = 400

water = pygame.rect(400, 300, 200, 100)
walls = pygame.rect(300, 200, 30, 300)
play_button = pygame.rect(400, 400, 200, 80)
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

                if event.key == pygame.K_SPACE:
                    charging = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE:

                    charging = False

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

    screen.blit(text_4, (width // 2 - text_4.get_width() // 2, 600))


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

    if state == MENU:
        draw_menu()
    elif state == GAME:
        controls_page()

    pygame.display.flip()

pygame.quit()
sys.exit()
