import pygame
import Game
import os
import records
import secondary_menu
import settings

WHITE = (255, 255, 255)


pygame.font.init()
font = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)
TITLE_FONT = pygame.font.Font(os.path.join('fonts', 'FreshLychee-mLoK2.ttf'), 45)
NAME_FONT = pygame.font.Font(os.path.join('fonts', 'FreshLychee-mLoK2.ttf'), 55)

SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 55)

user_text = ''
num_of_players = 1


def draw_main_menu(hard_rect, normal_rect, easy_rect, records_rect, settings_rect):
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

    WIN.blit(BG, (0, 0))  # Display background

    middle_height = int(HEIGHT / 2 - 50)

    def draw_rect(rect, text, font, border, fix_x, fix_y, color=WHITE):
        pygame.draw.rect(WIN, color, rect, border)
        label = font.render(text, 1, color)  # Create hard label
        WIN.blit(label, (rect.x + fix_x, rect.y + fix_y))  # Display label in the middle

    def mid_width(obj):
        return int(WIDTH / 2 - obj.get_width() / 2)


    # play_color = (73, 114, 252)
    records_color = (163, 128, 222)
    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    draw_rect(records_rect, 'records', SMALL_TITLE_FONT, 2, 10, 15, records_color)
    draw_rect(settings_rect, 'setting', SMALL_TITLE_FONT, 2, 10, 15, records_color)

    titel_label = font.render("SPACE SHOOTER", 1, WHITE)  # Create begin label
    WIN.blit(titel_label, (mid_width(titel_label), 80))  # Display label in the middle

    # Labels
    name_label = TITLE_FONT.render("Enter your name: ", 1, WHITE)  # Create begin label
    WIN.blit(name_label, (mid_width(name_label), 400))  # Display label in the middle

    # Name input
    text_surface = NAME_FONT.render(user_text, True, WHITE)
    WIN.blit(text_surface, (mid_width(text_surface), 450))

    if len(user_text) > 1:
        start_game_label = TITLE_FONT.render("Click on the desire difficulty", 1, WHITE)  # Create begin label
        WIN.blit(start_game_label, (mid_width(start_game_label), middle_height + 180))  # Display label in the middle

        draw_rect(easy_rect, 'Easy', LARGE_FONT, 2, 30, 60, easy_color)
        draw_rect(normal_rect, 'Normal', LARGE_FONT, 2, 10, 60, normal_color)
        draw_rect(hard_rect, 'Hard', LARGE_FONT, 2, 30, 60, hard_color)


def main_menu():
    global user_text, num_of_players
    run = True
    rect_width = 150
    rect_height = 150
    mode = None

    MIDDLE_WIDTH = 500
    middle_height = 350
    # play_rect = pygame.Rect(MIDDLE_WIDTH - 60, 280, 120, 60)
    # Creating all the mode rectangles

    records_rect = pygame.Rect(MIDDLE_WIDTH - 60, 230, 120, 60)
    settings_rect = pygame.Rect(MIDDLE_WIDTH - 60, 300, 120, 60)
    hard_rect = pygame.Rect(int(MIDDLE_WIDTH + rect_width), middle_height + 250, rect_width, rect_height)
    normal_rect = pygame.Rect(int(MIDDLE_WIDTH - rect_width / 2), middle_height + 250, rect_width, rect_height)
    easy_rect = pygame.Rect(int(MIDDLE_WIDTH - 2 * rect_width), middle_height + 250, rect_width, rect_height)

    while run:
        # draw all the labels on the screen
        draw_main_menu(hard_rect, normal_rect, easy_rect, records_rect, settings_rect)

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
                    if normal_rect.collidepoint(event.pos):
                        mode = 'normal'
                    if hard_rect.collidepoint(event.pos):
                        mode = 'hard'
                    if mode is not None:
                        score = Game.start(user_text, mode, num_of_players)
                        if score != 0:
                            records.add_to_db(user_text, mode, score)
                            run = secondary_menu.menu(user_text, score, mode, num_of_players)
                        mode = None
                if records_rect.collidepoint(event.pos):
                    run = records.records_table()
                    mode = None
                if settings_rect.collidepoint(event.pos):
                    run, num_of_players = settings.main(num_of_players)
                    mode = None
            if event.type == pygame.KEYDOWN:
                if len(user_text) < 20:
                    if event.unicode.isalpha() or event.key == pygame.K_SPACE:
                        user_text += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
    pygame.quit()


main_menu()
