import pygame
import sys
import math

pygame.init()

background_color = (79, 121, 66)
dark_green = (43, 92, 34)
white = (255, 255, 255)
black = (0, 0, 0)

width, height = (1000, 800)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mini_Golf_Game")

title_font = pygame.font.SysFont("airal", 75)
button_font = pygame.font.SysFont("arial", 40)

play_button = pygame.Rect(400, 375, 200, 80)
quit_button = pygame.Rect(400, 475, 200, 80)

MENU = "menu"
CONTROLS = "controls"
GAME = "game"
WIN = "win"

state = MENU
clock = pygame.time.Clock()

ball_x = 150
ball_y = 400
ball_radius = 15

ball_speed_x = 0
ball_speed_y = 0

hole_x = 850
hole_y = 400
hole_radius = 20

angle = 0
power = 0
charging = False

ball_moving = False

strokes = 0


def draw_checkerboard(tile_size=50):
    for row in range(0, height, tile_size):
        for col in range(0, width, tile_size):
            if (row // tile_size + col // tile_size) % 2 == 0:
                color = background_color
            else:
                color = dark_green
            pygame.draw.rect(screen, color, (col, row, tile_size, tile_size))


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


def controls_page():
    draw_checkerboard()

    title = title_font.render("Controls", True, white)
    screen.blit(title, (width // 2 - title.get_width() // 2, 200))

    text_1 = button_font.render("Use the arrow keys to aim left and right", True, white)

    screen.blit(text_1, (width // 2 - text_1.get_width() // 2, 300))

    text_2 = button_font.render("Hold SPACE to determine power", True, white)
    screen.blit(text_2, (width // 2 - text_2.get_width() // 2, 400))

    text_3 = button_font.render("Release SPACE to shoot", True, white)
    screen.blit(text_3, (width // 2 - text_3.get_width() // 2, 500))

    text_4 = button_font.render("Press ENTER to continue", True, white)
    screen.blit(text_3, (width // 2 - text_3.get_width() // 2, 600))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    state = GAME
                if quit_button.collidepoint(event.pos):
                    running = False

    if state == MENU:
        draw_menu()
    elif state == GAME:
        controls_page()

    pygame.display.flip()

pygame.quit()
sys.exit()

# NEED REQUIEREMENTS.TXT FILE FOR PYGAME
