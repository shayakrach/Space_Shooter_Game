import pygame
import os
import sqlite3


WHITE = (255, 255, 255)


font = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)

pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 45)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)


def print_records(mode,WIN):
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
    WIN.blit(mode_label, (int(490 - mode_label.get_width() / 2), 260))  # Display label in the middle

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
        WIN.blit(name_label, ((x + 50) + 100 - name_label.get_width() / 2, y + 15))  # Display label in the middle

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
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))
    mode = sent_mode
    rect_width = 150
    rect_height = 150

    def draw_rect(rect, text, font, border, fix_x, fix_y, color=WHITE):
        pygame.draw.rect(WIN, color, rect, border)
        label = font.render(text, 1, color)  # Create hard label
        WIN.blit(label, (rect.x + fix_x, rect.y + fix_y))  # Display label in the middle

    back_rect = pygame.Rect(50, 50, 120, 60)
    hard_rect = pygame.Rect(int(WIDTH / 2 + rect_width), int(HEIGHT / 2 +200), rect_width, rect_height)
    normal_rect = pygame.Rect(int(WIDTH / 2 - rect_width / 2), int(HEIGHT / 2 +200), rect_width, rect_height)
    easy_rect = pygame.Rect(int(WIDTH / 2- 2 * rect_width), int(HEIGHT / 2 +200), rect_width, rect_height)

    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    up_bar_color = (163, 128, 222)

    borders = [0, 0, 0]

    while True:
        WIN.blit(BG, (0, 0))  # Display background

        title_label = font.render("RECORDS", 1, WHITE)  # Create begin label
        WIN.blit(title_label, (int(WIDTH / 2 - title_label.get_width() / 2), 80))  # Display label in the middle

        draw_rect(back_rect, 'back', SMALL_TITLE_FONT, 2, 25, 20, up_bar_color)
        draw_rect(easy_rect, 'Easy', LARGE_FONT,  2 + borders[0], 25, 60,  easy_color)
        draw_rect(normal_rect, 'Normal', NAME_FONT,  2 + borders[1], 10, 60, normal_color)
        draw_rect(hard_rect, 'Hard', LARGE_FONT,  2 + borders[2], 25, 60, hard_color)

        if mode is not None:
            print_records(mode, WIN)
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
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
