import pygame
import sys
import math

pygame.init()

# Colors
background_color = (79, 121, 66)
dark_green = (43, 92, 34)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (150, 75, 0)
blue = (0, 100, 255)

# Screen
width, height = (1000, 800)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mini Golf Physics Test")

# Fonts
title_font = pygame.font.SysFont("arial", 70)
button_font = pygame.font.SysFont("arial", 40)

clock = pygame.time.Clock()

# States
CONTROLS = "controls"
GAME = "game"

state = CONTROLS

# Ball start position
start_x = 200
start_y = 400

# Ball variables
ball_x = start_x
ball_y = start_y

ball_radius = 15

ball_speed_x = 0
ball_speed_y = 0

ball_moving = False

# Aim variables
angle = 0
power = 0
charging = False

# Stroke counter
strokes = 0

# Walls
walls = [
    pygame.Rect(300, 200, 30, 400),
    pygame.Rect(500, 0, 30, 500),
    pygame.Rect(700, 300, 30, 500),
]

# Water hazards
water_hazards = [pygame.Rect(350, 650, 200, 80), pygame.Rect(550, 150, 150, 80)]


def draw_checkerboard(tile_size=50):

    for row in range(0, height, tile_size):
        for col in range(0, width, tile_size):

            if (row // tile_size + col // tile_size) % 2 == 0:
                color = background_color
            else:
                color = dark_green

            pygame.draw.rect(screen, color, (col, row, tile_size, tile_size))


def controls_page():

    draw_checkerboard()

    title = title_font.render("Controls", True, white)

    screen.blit(title, (width // 2 - title.get_width() // 2, 150))

    text_1 = button_font.render("LEFT and RIGHT arrows to aim", True, white)

    screen.blit(text_1, (width // 2 - text_1.get_width() // 2, 300))

    text_2 = button_font.render("Hold SPACE to gain power", True, white)

    screen.blit(text_2, (width // 2 - text_2.get_width() // 2, 400))

    text_3 = button_font.render("Release SPACE to shoot", True, white)

    screen.blit(text_3, (width // 2 - text_3.get_width() // 2, 500))

    text_4 = button_font.render("Press ENTER to start", True, white)

    screen.blit(text_4, (width // 2 - text_4.get_width() // 2, 600))


def draw_game():

    draw_checkerboard()

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, brown, wall)

    # Draw water hazards
    for water in water_hazards:
        pygame.draw.rect(screen, blue, water)

    # Draw ball
    pygame.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_radius)

    # Draw aiming line
    if not ball_moving:

        line_length = 100

        end_x = ball_x + math.cos(math.radians(angle)) * line_length
        end_y = ball_y - math.sin(math.radians(angle)) * line_length

        pygame.draw.line(screen, white, (ball_x, ball_y), (end_x, end_y), 5)

    # Draw power bar
    pygame.draw.rect(screen, white, (50, 50, power * 4, 30))

    power_text = button_font.render("Power", True, white)

    screen.blit(power_text, (50, 10))

    # Stroke counter
    stroke_text = button_font.render("Strokes: " + str(strokes), True, white)

    screen.blit(stroke_text, (700, 20))


def move_ball():

    global ball_x
    global ball_y
    global ball_speed_x
    global ball_speed_y
    global ball_moving
    global strokes

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Friction
    ball_speed_x *= 0.99
    ball_speed_y *= 0.99

    # Stop ball eventually
    if abs(ball_speed_x) < 0.1 and abs(ball_speed_y) < 0.1:

        ball_speed_x = 0
        ball_speed_y = 0

        ball_moving = False

    # Bounce off screen borders
    if ball_x <= ball_radius or ball_x >= width - ball_radius:
        ball_speed_x *= -1

    if ball_y <= ball_radius or ball_y >= height - ball_radius:
        ball_speed_y *= -1

    # Ball collision rectangle
    ball_rect = pygame.Rect(
        ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2
    )

    # Wall collisions
    for wall in walls:

        if ball_rect.colliderect(wall):

            # Bounce horizontally
            if ball_rect.centerx < wall.left or ball_rect.centerx > wall.right:
                ball_speed_x *= -1

            # Bounce vertically
            if ball_rect.centery < wall.top or ball_rect.centery > wall.bottom:
                ball_speed_y *= -1

    # Water hazard collisions
    for water in water_hazards:

        # Closest point on water rectangle
        closest_x = max(water.left, min(ball_x, water.right))
        closest_y = max(water.top, min(ball_y, water.bottom))

        # Distance from center of ball
        distance_x = ball_x - closest_x
        distance_y = ball_y - closest_y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        # About 75% of ball must touch water
        if distance < ball_radius / 4:

            # Penalty stroke
            strokes += 1

            # Reset ball position
            ball_x = start_x
            ball_y = start_y

            # Stop movement
            ball_speed_x = 0
            ball_speed_y = 0

            ball_moving = False


running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Controls screen
        if state == CONTROLS:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    state = GAME

        # Game screen
        elif state == GAME:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and not ball_moving:
                    charging = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE and not ball_moving:

                    charging = False
                    ball_moving = True

                    strokes += 1

                    ball_speed_x = math.cos(math.radians(angle)) * (power / 2.5)

                    ball_speed_y = -math.sin(math.radians(angle)) * (power / 2.5)

                    power = 0

    # Game logic
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
    if state == CONTROLS:
        controls_page()

    elif state == GAME:
        draw_game()

    pygame.display.flip()

pygame.quit()
sys.exit()
