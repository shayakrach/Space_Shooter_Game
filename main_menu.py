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

user_text = ''


def add_to_db(dif, score):
    global user_text
    conn = sqlite3.connect('scores.db')

    c = conn.cursor()

    # need to add a time later
    '''c.execute("""CREATE TABLE scores (
                name TEXT,
                dif INTEGER,
                score REAL
                )""")
    '''
    if user_text == '':
        user_text = 'Anonymous'
    c.execute("INSERT INTO scores VALUES ('{}','{}','{}')".format(user_text, dif, score))
    conn.commit()

    c.execute("SELECT * FROM scores")

    print(c.fetchmany(13))

    conn.commit()

    conn.close()


def main_menu():
    global user_text
    run = True
    rect_width = 150
    rect_height = 150
    MIDDLE_WIDTH = int(WIDTH / 2)
    hard_rect = pygame.Rect(int(MIDDLE_WIDTH + rect_width), middle_height+200, rect_width,rect_height)
    normal_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width/2), middle_height+200, rect_width,rect_height)
    easy_rect = pygame.Rect(int(MIDDLE_WIDTH - 2*rect_width), middle_height+200, rect_width,rect_height)

    color = pygame.Color('lightskyblue3')

    while run:
        WIN.blit((BG), (0, 0))  # Display background

        # Name input
        text_surface = NAME_FONT.render(user_text, True, WHITE)
        WIN.blit(text_surface, (int(MIDDLE_WIDTH - text_surface.get_width() / 3 - 40), middle_height - 70))

        # Labels
        name_label = TITLE_FONT.render("Enter your name: ", 1, WHITE)  # Create begin label
        WIN.blit(name_label,
                 (int(MIDDLE_WIDTH - name_label.get_width() / 2), middle_height - 150))  # Display label in the middle

        if len(user_text) > 1:
            start_game_label = TITLE_FONT.render("Click on the desire difficulty", 1, WHITE)  # Create begin label
            middle_width = int(WIDTH / 2 - start_game_label.get_width() / 2)
            WIN.blit(start_game_label, (middle_width, middle_height + 100))  # Display label in the middle

            pygame.draw.rect(WIN, color, easy_rect, 3)
            easy_label = LARGE_FONT.render("Easy", 1, color)  # Create hard label
            WIN.blit(easy_label,(easy_rect.x + 25,easy_rect.y + 60))  # Display label in the middle

            pygame.draw.rect(WIN, color, normal_rect, 3)
            normal_label = NAME_FONT.render("Normal", 1, color)  # Create hard label
            WIN.blit(normal_label, (normal_rect.x + 10, normal_rect.y + 60))  # Display label in the middle

            pygame.draw.rect(WIN, color, hard_rect, 3)
            hard_label = LARGE_FONT.render("Hard", 1, color)  # Create hard label
            WIN.blit(hard_label, (hard_rect.x + 25, hard_rect.y + 60))  # Display label in the middle






        '''

        difficulty_game_label = TITLE_FONT.render("1-easy, ... , 9-hard", 1, WHITE)  # Create begin label
        middle_width = int(WIDTH / 2 - difficulty_game_label.get_width() / 2)
        WIN.blit(difficulty_game_label, (middle_width, middle_height + 150))  # Display label in the middle
        '''

        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and user_text != '':
                if easy_rect.collidepoint(event.pos):
                    dif, new_record = Game.start(user_text, 'easy')
                    add_to_db(dif, new_record)
                    after_game_menu(new_record)
                    run = False
                if normal_rect.collidepoint(event.pos):
                    dif, new_record = Game.start(user_text, 'normal')
                    add_to_db(dif, new_record)
                    after_game_menu(new_record)
                    run = False
                if hard_rect.collidepoint(event.pos):
                    dif, new_record = Game.start(user_text, 'hard')
                    add_to_db(dif, new_record)
                    after_game_menu(new_record)
                    run = False
            if event.type == pygame.KEYDOWN:
                if len(user_text) < 20:
                    if event.unicode.isalpha() or event.key == pygame.K_SPACE:
                        user_text += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

    pygame.quit()


def after_game_menu(record):
    run = True
    is_new_record = False
    current_score_label = None

    while run:
        WIN.blit(BG, (0, 0))  # Display background

        # Labels
        broke_record_label = TITLE_FONT.render("Your broke the record!!", 1, WHITE)  # Create record label
        record_label = TITLE_FONT.render("Your record: {:.2f}".format(record), 1, WHITE)  # Create record label

        if is_new_record:
            middle_width = int(WIDTH / 2 - broke_record_label.get_width() / 2)
            WIN.blit(broke_record_label, (middle_width, middle_height - 150))  # Display label in the middle

        if record > 0:
            middle_width = int(WIDTH / 2 - record_label.get_width() / 2)
            WIN.blit(record_label, (middle_width, middle_height - 100))  # Display label in the middle

        if current_score_label is not None:
            middle_width = int(WIDTH / 2 - current_score_label.get_width() / 2)
            WIN.blit(current_score_label, (middle_width, HEIGHT - 70))  # Display label in the middle

        start_game_label = TITLE_FONT.render("Click <1-9> to start the game", 1, WHITE)  # Create begin label
        middle_width = int(WIDTH / 2 - start_game_label.get_width() / 2)
        WIN.blit(start_game_label, (middle_width, middle_height + 100))  # Display label in the middle

        difficulty_game_label = TITLE_FONT.render("1-easy, ... , 9-hard", 1, WHITE)  # Create begin label
        middle_width = int(WIDTH / 2 - difficulty_game_label.get_width() / 2)
        WIN.blit(difficulty_game_label, (middle_width, middle_height + 150))  # Display label in the middle
        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_9, pygame.K_8, pygame.K_7, pygame.K_6, pygame.K_5, pygame.K_4, pygame.K_3,
                                 pygame.K_2, pygame.K_1]:
                    dif, new_record = Game.start(user_text, event.unicode)
                    add_to_db(dif, new_record)
                    # Create current score label
                    current_score_label = SMALL_TITLE_FONT.render("current score: {:.2f}".format(new_record), 1, WHITE)
                    is_new_record = new_record > record
                    record = max(record, new_record)


main_menu()
