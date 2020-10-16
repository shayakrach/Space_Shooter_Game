import pygame
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

def print_records(mode):
    conn = sqlite3.connect('scores.db')

    c = conn.cursor()

    c.execute("""SELECT name, score
                 FROM scores
                 WHERE mode = '{}'
                 ORDER BY score DESC""".format(mode))

    table = c.fetchmany(3)

    pos_rect = pygame.Rect(320, 240, 350, 60)
    pygame.draw.rect(WIN, WHITE, pos_rect, 2)
    mode_label = SMALL_TITLE_FONT.render(mode, 1, WHITE)  # Create hard label
    WIN.blit(mode_label, (int(490 -mode_label.get_width()/2) , 260))  # Display label in the middle

    y = 300
    for pos, line in enumerate(table):
        x = 320

        pos_rect = pygame.Rect(x, y, 50, 60)
        pygame.draw.rect(WIN, WHITE, pos_rect, 2)
        pos_label = SMALL_TITLE_FONT.render(str(pos + 1), 1, WHITE)  # Create hard label
        WIN.blit(pos_label, (x + 17, y + 17))  # Display label in the middle

        name_rect = pygame.Rect(x + 50, y, 200, 60)
        pygame.draw.rect(WIN, WHITE, name_rect, 2)
        name_label = SMALL_TITLE_FONT.render(str(line[0]), 1, WHITE)  # Create hard label
        WIN.blit(name_label, (x + 110, y + 15))  # Display label in the middle

        score_rect = pygame.Rect(x + 250, y, 100, 60)
        pygame.draw.rect(WIN, WHITE, score_rect, 2)
        name_label = SMALL_TITLE_FONT.render(str(line[1]), 1, WHITE)  # Create hard label
        WIN.blit(name_label, (x + 275, y + 17))  # Display label in the middle

        y += 60

    conn.close()


def get_record(mode):
    conn = sqlite3.connect('scores.db')

    c = conn.cursor()

    c.execute("""SELECT score
                     FROM scores
                     WHERE mode = '{}'
                     ORDER BY score DESC""".format(mode))

    record = c.fetchone()

    conn.close()

    if record is None:
        return 0
    return float(record[0])


def add_to_db(name, mode, score):
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

    c.execute("INSERT INTO scores VALUES ('{}','{}',{})".format(name, mode, score))

    conn.commit()

    conn.close()


def records_table(sent_mode=None):
    mode = sent_mode
    rect_width = 150
    rect_height = 150

    menu_rect = pygame.Rect(50, 50, 120, 60)
    hard_rect = pygame.Rect(int(MIDDLE_WIDTH + rect_width), middle_height + 250, rect_width, rect_height)
    normal_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width / 2), middle_height + 250, rect_width, rect_height)
    easy_rect = pygame.Rect(int(MIDDLE_WIDTH - 2 * rect_width), middle_height + 250, rect_width, rect_height)

    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    up_bar_color = (163, 128, 222)
    pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)

    borders = [0, 0, 0]

    while True:
        WIN.blit(BG, (0, 0))  # Display background

        titel_label = font.render("RECORDS", 1, WHITE)  # Create begin label
        WIN.blit(titel_label, (int(MIDDLE_WIDTH - titel_label.get_width() / 2), 80))  # Display label in the middle
        pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)
        menu_label = SMALL_TITLE_FONT.render("menu", 1, up_bar_color)  # Create hard label
        WIN.blit(menu_label, (menu_rect.x + 20, menu_rect.y + 15))  # Display label in the middle

        pygame.draw.rect(WIN, easy_color, easy_rect, 2 + borders[0])
        easy_label = LARGE_FONT.render("Easy", 1, easy_color)  # Create hard label
        WIN.blit(easy_label, (easy_rect.x + 25, easy_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, normal_color, normal_rect, 2 + borders[1])
        normal_label = NAME_FONT.render("Normal", 1, normal_color)  # Create hard label
        WIN.blit(normal_label, (normal_rect.x + 10, normal_rect.y + 60))  # Display label in the middle

        pygame.draw.rect(WIN, hard_color, hard_rect, 2 + borders[2])
        hard_label = LARGE_FONT.render("Hard", 1, hard_color)  # Create hard label
        WIN.blit(hard_label, (hard_rect.x + 25, hard_rect.y + 60))  # Display label in the middle

        if mode is not None:
            print_records(mode)
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    return True
                if easy_rect.collidepoint(event.pos):
                    mode = 'easy'
                    borders = [4, 0, 0]
                if normal_rect.collidepoint(event.pos):
                    mode = 'normal'
                    borders = [0, 4, 0]
                if hard_rect.collidepoint(event.pos):
                    mode = 'hard'
                    borders = [0, 0, 4]
