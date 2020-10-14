import pygame
import Game
import os
import sqlite3

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

record = 5


def print_records():
    conn = sqlite3.connect('scores.db')

    c = conn.cursor()

    c.execute("""SELECT name, score
                 FROM scores
                 WHERE mode = 'hard'
                 ORDER BY score DESC""")

    table = c.fetchmany(5)

    y = 300
    for pos, line in enumerate(table):
        x = 300

        pos_rect = pygame.Rect(x, y, 50, 60)
        pygame.draw.rect(WIN, WHITE, pos_rect, 2)
        pos_label = SMALL_TITLE_FONT.render(str(pos+1), 1, WHITE)  # Create hard label
        WIN.blit(pos_label, (x+17, y+17))  # Display label in the middle


        name_rect = pygame.Rect(x+50, y, 120, 60)
        pygame.draw.rect(WIN, WHITE, name_rect, 2)
        name_label = SMALL_TITLE_FONT.render(str(line[0]), 1, WHITE)  # Create hard label
        WIN.blit(name_label, (x+90, y+15))  # Display label in the middle

        score_rect = pygame.Rect(x+170, y, 100, 60)
        pygame.draw.rect(WIN, WHITE, score_rect, 2)
        name_label = SMALL_TITLE_FONT.render(str(line[1]), 1, WHITE)  # Create hard label
        WIN.blit(name_label, (x+200, y+15))  # Display label in the middle

        y += 60

    conn.commit()

    conn.close()


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
    '''
    if user_text == '':
        user_text = 'Anonymous'
        
    c.execute("INSERT INTO scores VALUES ('{}','{}',{})".format(user_text, mode, score))

    conn.commit()

    conn.close()


def racords_table():

    menu_rect = pygame.Rect(50, 50, 120, 60)

    up_bar_color = (163, 128, 222)
    pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)


    while True:
        WIN.blit(BG, (0, 0))  # Display background
        pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)
        menu_label = SMALL_TITLE_FONT.render("menu", 1, up_bar_color)  # Create hard label
        WIN.blit(menu_label, (menu_rect.x + 20, menu_rect.y + 15))  # Display label in the middle


        print_records()
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    return True


def draw_main_menu(hard_rect, normal_rect, easy_rect, records_rect, play_rect, borders):
    WIN.blit(BG, (0, 0))  # Display background

    play_color = (73, 114, 252)
    records_color = (163, 128, 222)
    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    pygame.draw.rect(WIN, records_color, records_rect, 2)
    records_label = SMALL_TITLE_FONT.render("records", 1,records_color)  # Create hard label
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
    WIN.blit(name_label,(int(MIDDLE_WIDTH - name_label.get_width() / 2), 200))  # Display label in the middle

    # Name input
    text_surface = NAME_FONT.render(user_text, True, WHITE)
    WIN.blit(text_surface, (int(MIDDLE_WIDTH - text_surface.get_width() / 2.2 - 5), 250))


    if len(user_text) > 1:
        start_game_label = TITLE_FONT.render("Click on the desire difficulty", 1, WHITE)  # Create begin label
        middle_width = int(WIDTH / 2 - start_game_label.get_width() / 2)
        WIN.blit(start_game_label, (middle_width, middle_height + 180))  # Display label in the middle

        pygame.draw.rect(WIN, easy_color, easy_rect, 2 + borders[0])
        easy_label = LARGE_FONT.render("Easy", 1, easy_color)  # Create hard label
        WIN.blit(easy_label, (easy_rect.x + 25, easy_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, normal_color, normal_rect,2 + borders[1])
        normal_label = NAME_FONT.render("Normal", 1, normal_color)  # Create hard label
        WIN.blit(normal_label, (normal_rect.x + 10, normal_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, hard_color, hard_rect, 2 + borders[2])
        hard_label = LARGE_FONT.render("Hard", 1, hard_color)  # Create hard label
        WIN.blit(hard_label, (hard_rect.x + 25, hard_rect.y + 60))  # Display label in the middle


def draw_after_game_menu(play_again_rect, menu_rect, records_rect, score, mode):
    WIN.blit(BG, (0, 0))  # Display background
    play_again_color = (73, 114, 252)
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
    menu_label = SMALL_TITLE_FONT.render("menu", 1, up_bar_color)  # Create hard label
    WIN.blit(menu_label, (menu_rect.x + 20, menu_rect.y + 15))  # Display label in the middle

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
                if records_rect.collidepoint(event.pos):
                    return racords_table()


def main_menu():
    global user_text
    run = True
    rect_width = 150
    rect_height = 150
    mode = None
    borders = [0, 0, 0]

    # Creating all the mode rectangles
    play_rect = pygame.Rect(MIDDLE_WIDTH - 60, 430, 120, 60)
    records_rect = pygame.Rect(MIDDLE_WIDTH - 60, 350, 120, 60)
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
                        add_to_db(mode, score)
                        run = after_game_menu(score, mode)
                if records_rect.collidepoint(event.pos):
                    run = racords_table()
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
