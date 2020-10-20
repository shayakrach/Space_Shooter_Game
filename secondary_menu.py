import pygame
import os
import Game
import records


WHITE = (255, 255, 255)

pygame.font.init()
font = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)


TITLE_FONT = pygame.font.Font(os.path.join('fonts', 'JustMyType-KePl.ttf'), 40)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 35)
LARGE_FONT = pygame.font.Font(None, 60)
RECORD_FONT = pygame.font.Font(os.path.join('fonts', 'ARCADECLASSIC.TTF'), 50)


def draw_menu(play_again_rect, menu_rect, records_rect, score, mode):

    WIDTH, HEIGHT = 1000, 800
    middle_height = int(HEIGHT / 2 - 50)

    def draw_rect(rect, text, font, border, fix_x, fix_y, color=WHITE):
        pygame.draw.rect(WIN, color, rect, border)
        label = font.render(text, 1, color)  # Create hard label
        WIN.blit(label, (rect.x + fix_x, rect.y + fix_y))  # Display label in the middle

    def mid_width(obj):
        return int(WIDTH / 2 - obj.get_width() / 2)

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0))  # Display background
    play_again_color = (73, 114, 252)
    up_bar_color = (163, 128, 222)
    # Labels
    broke_record_label = RECORD_FONT.render("You    broke    the    record!!", 1, WHITE)  # Create record label
    if score == records.get_record(mode):
        WIN.blit(broke_record_label, (mid_width(broke_record_label), middle_height - 150))  # Display label in the middle

    mode_label = TITLE_FONT.render("Mode: {}".format(mode), 1, WHITE)  # Create record label
    WIN.blit(mode_label, (mid_width(mode_label), middle_height - 60))  # Display label in the middle

    score_label = TITLE_FONT.render("Score: {}".format(score), 1, WHITE)  # Create record label
    WIN.blit(score_label, (mid_width(score_label), middle_height))  # Display label in the middle

    draw_rect(play_again_rect, 'Play', LARGE_FONT, 2, 30, 30,play_again_color)
    again_label = LARGE_FONT.render("again", 1, play_again_color)  # Create hard label
    WIN.blit(again_label, (play_again_rect.x + 20, play_again_rect.y + 90))  # Display label in the middle

    draw_rect(menu_rect, 'menu', SMALL_TITLE_FONT, 2, 20, 15, up_bar_color)
    draw_rect(records_rect, 'records', SMALL_TITLE_FONT, 2, 10, 15, up_bar_color)


def menu(name, score, mode, num_of_players):
    rect_width = 150
    rect_height = 150

    play_again_rect = pygame.Rect(int(500 - rect_width / 2), 550, rect_width, rect_height)
    menu_rect = pygame.Rect(50, 50, 120, 60)
    records_rect = pygame.Rect(830, 50, 120, 60)

    while True:
        draw_menu(play_again_rect, menu_rect, records_rect, score, mode)
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    score = Game.start(name, mode, num_of_players)
                    if score == 0:
                        return True
                    records.add_to_db(name, mode, score)
                if menu_rect.collidepoint(event.pos):
                    return True
                if records_rect.collidepoint(event.pos):
                    records.records_table(mode)
