import pygame
import Game
import os
import records
import secondary_menu

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

user_text = ''


def draw_main_menu(hard_rect, normal_rect, easy_rect, records_rect, play_rect, borders):
    WIN.blit(BG, (0, 0))  # Display background

    play_color = (73, 114, 252)
    records_color = (163, 128, 222)
    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    pygame.draw.rect(WIN, records_color, records_rect, 2)
    records_label = SMALL_TITLE_FONT.render("records", 1, records_color)  # Create hard label
    WIN.blit(records_label, (records_rect.x + 10, records_rect.y + 15))  # Display label in the middle

    if 4 in borders:
        pygame.draw.rect(WIN, play_color, play_rect, 2)
        records_label = SMALL_TITLE_FONT.render("play", 1, play_color)  # Create hard label
        WIN.blit(records_label, (play_rect.x + 30, play_rect.y + 15))  # Display label in the middle

    titel_label = font.render("SPACE SHOOTER", 1, WHITE)  # Create begin label
    WIN.blit(titel_label,
             (int(MIDDLE_WIDTH - titel_label.get_width() / 2), 80))  # Display label in the middle

    # Labels
    name_label = TITLE_FONT.render("Enter your name: ", 1, WHITE)  # Create begin label
    WIN.blit(name_label, (int(MIDDLE_WIDTH - name_label.get_width() / 2), 410))  # Display label in the middle

    # Name input
    text_surface = NAME_FONT.render(user_text, True, WHITE)
    WIN.blit(text_surface, (int(MIDDLE_WIDTH - text_surface.get_width() / 2.2 - 5), 460))

    if len(user_text) > 1:
        start_game_label = TITLE_FONT.render("Click on the desire difficulty", 1, WHITE)  # Create begin label
        middle_width = int(WIDTH / 2 - start_game_label.get_width() / 2)
        WIN.blit(start_game_label, (middle_width, middle_height + 180))  # Display label in the middle

        pygame.draw.rect(WIN, easy_color, easy_rect, 2 + borders[0])
        easy_label = LARGE_FONT.render("Easy", 1, easy_color)  # Create hard label
        WIN.blit(easy_label, (easy_rect.x + 25, easy_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, normal_color, normal_rect, 2 + borders[1])
        normal_label = NAME_FONT.render("Normal", 1, normal_color)  # Create hard label
        WIN.blit(normal_label, (normal_rect.x + 10, normal_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, hard_color, hard_rect, 2 + borders[2])
        hard_label = LARGE_FONT.render("Hard", 1, hard_color)  # Create hard label
        WIN.blit(hard_label, (hard_rect.x + 25, hard_rect.y + 60))  # Display label in the middle


def main_menu():
    global user_text
    run = True
    rect_width = 150
    rect_height = 150
    mode = None
    borders = [0, 0, 0]

    # Creating all the mode rectangles
    play_rect = pygame.Rect(MIDDLE_WIDTH - 60, 280, 120, 60)
    records_rect = pygame.Rect(MIDDLE_WIDTH - 60, 200, 120, 60)
    hard_rect = pygame.Rect(int(MIDDLE_WIDTH + rect_width), middle_height + 250, rect_width, rect_height)
    normal_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width / 2), middle_height + 250, rect_width, rect_height)
    easy_rect = pygame.Rect(int(MIDDLE_WIDTH - 2 * rect_width), middle_height + 250, rect_width, rect_height)

    while run:
        # draw all the labels on the screen
        draw_main_menu(hard_rect, normal_rect, easy_rect, records_rect, play_rect, borders)

        # Refresh the display
        pygame.display.update()

        # Checking all events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(user_text) > 1:
                    if easy_rect.collidepoint(event.pos):
                        mode = 'easy'
                        borders = [4, 0, 0]
                    if normal_rect.collidepoint(event.pos):
                        mode = 'normal'
                        borders = [0, 4, 0]
                    if hard_rect.collidepoint(event.pos):
                        mode = 'hard'
                        borders = [0, 0, 4]
                    if play_rect.collidepoint(event.pos) and mode is not None:
                        score = Game.start(user_text, mode)
                        records.add_to_db(user_text, mode, score)
                        run = secondary_menu.menu(user_text,score, mode)
                if records_rect.collidepoint(event.pos):
                    run = records.records_table()
            if event.type == pygame.KEYDOWN:
                if len(user_text) < 20:
                    if event.unicode.isalpha() or event.key == pygame.K_SPACE:
                        user_text += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                    if len(user_text) < 2:
                        borders = [0, 0, 0]
    pygame.quit()


main_menu()
