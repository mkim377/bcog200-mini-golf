import pygame
import sys

pygame.init()
background_color = (79, 121, 66)
(width, height) = (1000, 800)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mini_Golf_Game")
screen.fill(background_color)

title_font = pygame.font.SysFont("airal", 72)
button_font = pygame.font.SysFont("arial", 40)

play_button = pygame.Rect(400, 300, 200, 80)
quit_button = pygame.Rect(400, 420, 200, 80)
MENU = "menu"
GAME = "game"
state = MENU


def draw_menu():
    screen.fill(background_color)

    title_text = title_font.render("Mini Golf by Martin Kim", True, (255, 255, 255))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 120))

    pygame.draw.rect(screen, (0, 255, 0), play_button)
    play_text = button_font.render("PLAY", True, (0, 0, 0))
    screen.blit(play_text, (play_button.x + 60, play_button.y + 20))

    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = button_font.render("QUIT", True, (0, 0, 0))
    screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 20))


def run_game_placeholder():
    screen.fill((30, 30, 30))
    text = button_font.render("Mini Golf", True, (255, 255, 255))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))


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
        run_game_placeholder()

    pygame.display.flip()

pygame.quit()
sys.exit()
