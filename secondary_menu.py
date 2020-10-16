import pygame
import os
import Game
import records

WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

font = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)

pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 45)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)
middle_height = int(HEIGHT / 2 - 50)
MIDDLE_WIDTH = int(WIDTH / 2)


def mid_width(obj):
    return int(WIDTH / 2 - obj.get_width() / 2)


def draw_menu(play_again_rect, menu_rect, records_rect, score, mode):
    WIN.blit(BG, (0, 0))  # Display background
    play_again_color = (73, 114, 252)
    up_bar_color = (163, 128, 222)
    # Labels
    broke_record_label = TITLE_FONT.render("Your broke the record!!", 1, WHITE)  # Create record label
    if score == records.get_record(mode):
        WIN.blit(broke_record_label, (mid_width(broke_record_label), middle_height - 150))  # Display label in the middle

    mode_label = TITLE_FONT.render("Mode: {}".format(mode), 1, WHITE)  # Create record label
    WIN.blit(mode_label, (mid_width(mode_label), middle_height - 60))  # Display label in the middle

    score_label = TITLE_FONT.render("Score: {}".format(score), 1, WHITE)  # Create record label
    WIN.blit(score_label, (mid_width(score_label), middle_height))  # Display label in the middle

    pygame.draw.rect(WIN, play_again_color, play_again_rect, 3)
    play_label = LARGE_FONT.render("Play", 1, play_again_color)  # Create hard label
    WIN.blit(play_label, (play_again_rect.x + 30, play_again_rect.y + 30))  # Display label in the middle
    again_label = LARGE_FONT.render("again", 1, play_again_color)  # Create hard label
    WIN.blit(again_label, (play_again_rect.x + 20, play_again_rect.y + 90))  # Display label in the middle

    pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)
    menu_label = SMALL_TITLE_FONT.render("menu", 1, up_bar_color)  # Create hard label
    WIN.blit(menu_label, (menu_rect.x + 20, menu_rect.y + 15))  # Display label in the middle

    pygame.draw.rect(WIN, up_bar_color, records_rect, 2)
    records_label = SMALL_TITLE_FONT.render("records", 1, up_bar_color)  # Create hard label
    WIN.blit(records_label, (records_rect.x + 10, records_rect.y + 15))  # Display label in the middle


def menu(name, score, mode):
    rect_width = 150
    rect_height = 150

    play_again_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width / 2), middle_height + 200, rect_width, rect_height)
    menu_rect = pygame.Rect(50, 50, 120, 60)
    records_rect = pygame.Rect(WIDTH - 170, 50, 120, 60)

    while True:
        draw_menu(play_again_rect, menu_rect, records_rect,score, mode)
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    score = Game.start(name, mode)
                    if score == 0:
                        return True
                    records.add_to_db(name, mode, score)
                if menu_rect.collidepoint(event.pos):
                    return True
                if records_rect.collidepoint(event.pos):
                    return records.records_table(mode)
