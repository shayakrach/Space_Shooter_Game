import pygame
import Game
import os
import sqlite3

WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 45)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)
middle_height = int(HEIGHT / 2 - 50)
MIDDLE_WIDTH = int(WIDTH / 2)

user_text = ''

record = 5


def add_to_db(mode, score):
    global user_text
    conn = sqlite3.connect('scores.db')

    c = conn.cursor()
    '''
    # need to add a time later
    c.execute("""CREATE TABLE scores (
                name TEXT,
                mode TEXT,
                score REAL
                )""")

    if user_text == '':
        user_text = 'Anonymous'
    c.execute("INSERT INTO scores VALUES ('{}','{}','{}')".format(user_text, mode, score))
    conn.commit()

    c.execute("SELECT * FROM scores")

    print(c.fetchmany(13))
    '''
    conn.commit()

    conn.close()


def main_menu_events(hard_rect, normal_rect, easy_rect):
    # Checking all events
    global user_text
    mode = None

    print("WHAY")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and len(user_text) > 1:
            if easy_rect.collidepoint(event.pos):
                mode = 'easy'
            if normal_rect.collidepoint(event.pos):
                mode = 'normal'
            if hard_rect.collidepoint(event.pos):
                mode = 'hard'
            if mode is not None:
                score = Game.start(user_text, mode)
                add_to_db(mode, score)
                return after_game_menu(score, mode)
        if event.type == pygame.KEYDOWN:
            if len(user_text) < 20:
                if event.unicode.isalpha() or event.key == pygame.K_SPACE:
                    user_text += event.unicode
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
    return True


def draw_main_menu(hard_rect, normal_rect, easy_rect):
    WIN.blit(BG, (0, 0))  # Display background

    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    # Labels
    name_label = TITLE_FONT.render("Enter your name: ", 1, WHITE)  # Create begin label
    WIN.blit(name_label,
             (int(MIDDLE_WIDTH - name_label.get_width() / 2), middle_height - 150))  # Display label in the middle

    # Name input
    text_surface = NAME_FONT.render(user_text, True, WHITE)
    WIN.blit(text_surface, (int(MIDDLE_WIDTH - text_surface.get_width() / 2.5 - 25), middle_height - 70))

    if len(user_text) > 1:
        start_game_label = TITLE_FONT.render("Click on the desire difficulty", 1, WHITE)  # Create begin label
        middle_width = int(WIDTH / 2 - start_game_label.get_width() / 2)
        WIN.blit(start_game_label, (middle_width, middle_height + 100))  # Display label in the middle

        pygame.draw.rect(WIN, easy_color, easy_rect, 3)
        easy_label = LARGE_FONT.render("Easy", 1, easy_color)  # Create hard label
        WIN.blit(easy_label, (easy_rect.x + 25, easy_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, normal_color, normal_rect, 3)
        normal_label = NAME_FONT.render("Normal", 1, normal_color)  # Create hard label
        WIN.blit(normal_label, (normal_rect.x + 10, normal_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, hard_color, hard_rect, 3)
        hard_label = LARGE_FONT.render("Hard", 1, hard_color)  # Create hard label
        WIN.blit(hard_label, (hard_rect.x + 25, hard_rect.y + 60))  # Display label in the middle


def main_menu():
    run = True
    rect_width = 150
    rect_height = 150

    # Creating all the mode rectangles
    hard_rect = pygame.Rect(int(MIDDLE_WIDTH + rect_width), middle_height + 200, rect_width, rect_height)
    normal_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width / 2), middle_height + 200, rect_width, rect_height)
    easy_rect = pygame.Rect(int(MIDDLE_WIDTH - 2 * rect_width), middle_height + 200, rect_width, rect_height)

    while run:
        # draw all the labels on the screen
        draw_main_menu(hard_rect, normal_rect, easy_rect)

        # Refresh the display
        pygame.display.update()

        # Checking all events
        run = main_menu_events(hard_rect, normal_rect, easy_rect)

    pygame.quit()


def draw_after_game_menu(play_again_rect, menu_rect, records_rect, score, mode):
    WIN.blit(BG, (0, 0))  # Display background
    play_again_color = (70, 100, 229)
    up_bar_color = (163, 128, 222)
    # Labels
    broke_record_label = TITLE_FONT.render("Your broke the record!!", 1, WHITE)  # Create record label
    if score > record:
        middle_width = int(WIDTH / 2 - broke_record_label.get_width() / 2)
        WIN.blit(broke_record_label, (middle_width, middle_height - 150))  # Display label in the middle

    mode_label = TITLE_FONT.render("Mode: {}".format(mode), 1, WHITE)  # Create record label
    middle_width = int(WIDTH / 2 - mode_label.get_width() / 2)
    WIN.blit(mode_label, (middle_width, middle_height - 60))  # Display label in the middle

    score_label = TITLE_FONT.render("Score: {}".format(score), 1, WHITE)  # Create record label
    middle_width = int(WIDTH / 2 - score_label.get_width() / 2)
    WIN.blit(score_label, (middle_width, middle_height))  # Display label in the middle

    pygame.draw.rect(WIN, play_again_color, play_again_rect, 3)
    play_label = LARGE_FONT.render("Play", 1, play_again_color)  # Create hard label
    WIN.blit(play_label, (play_again_rect.x + 30, play_again_rect.y + 30))  # Display label in the middle
    again_label = LARGE_FONT.render("again", 1, play_again_color)  # Create hard label
    WIN.blit(again_label, (play_again_rect.x + 20, play_again_rect.y + 90))  # Display label in the middle

    pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)
    play_label = SMALL_TITLE_FONT.render("menu", 1, up_bar_color)  # Create hard label
    WIN.blit(play_label, (menu_rect.x + 20, menu_rect.y + 15))  # Display label in the middle

    pygame.draw.rect(WIN, up_bar_color, records_rect, 2)
    records_label = SMALL_TITLE_FONT.render("records", 1, up_bar_color)  # Create hard label
    WIN.blit(records_label, (records_rect.x + 10, records_rect.y + 15))  # Display label in the middle


def after_game_menu(score, mode):
    rect_width = 150
    rect_height = 150

    play_again_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width / 2), middle_height + 200, rect_width, rect_height)
    menu_rect = pygame.Rect(50, 50, 120, 60)
    records_rect = pygame.Rect(WIDTH - 170, 50, 120, 60)

    while True:
        draw_after_game_menu(play_again_rect, menu_rect, records_rect, score, mode)
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    score = Game.start(user_text, mode)
                    add_to_db(mode, score)
                if menu_rect.collidepoint(event.pos):
                    return True


main_menu()
