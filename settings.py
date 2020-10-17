import pygame
import os

WHITE = (255, 255, 255)

font = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)

pygame.font.init()
TITLE_FONT = pygame.font.Font(os.path.join('fonts', 'FreshLychee-mLoK2.ttf'), 45)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)


def main(num_of_players):
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

    def mid_width(obj):
        return int(WIDTH / 2 - obj.get_width() / 2)

    rect_width = 90
    rect_height = 40

    menu_rect = pygame.Rect(50, 50, 120, 60)
    one_rect = pygame.Rect(int(WIDTH / 2) - 100, 250, rect_width, rect_height)
    two_rect = pygame.Rect(int(WIDTH / 2) - 100 + rect_width, 250, rect_width, rect_height)

    hard_rect = pygame.Rect(int(WIDTH / 2 + rect_width), int(HEIGHT / 2 + 200), rect_width, rect_height)
    normal_rect = pygame.Rect(int(WIDTH / 2 - rect_width / 2), int(HEIGHT / 2 + 200), rect_width, rect_height)
    easy_rect = pygame.Rect(int(WIDTH / 2 - 2 * rect_width), int(HEIGHT / 2 + 200), rect_width, rect_height)

    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    up_bar_color = (163, 128, 222)
    pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)

    borders = [3, 0] if num_of_players == 1 else [0, 3]

    while True:
        WIN.blit(BG, (0, 0))  # Display background

        settings_label = font.render("SETTINGS", 1, WHITE)  # Create begin label
        WIN.blit(settings_label, (int(WIDTH / 2 - settings_label.get_width() / 2), 80))  # Display label in the middle

        pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)
        menu_label = SMALL_TITLE_FONT.render("menu", 1, up_bar_color)  # Create hard label
        WIN.blit(menu_label, (menu_rect.x + 25, menu_rect.y + 20))  # Display label in the middle

        num_players_label = TITLE_FONT.render("Num of players", 1, WHITE)  # Create begin label
        WIN.blit(num_players_label, (mid_width(num_players_label), one_rect.y - 80))  # Display label in the middle

        pygame.draw.rect(WIN, WHITE, one_rect, 2 + borders[0])
        one_label = SMALL_TITLE_FONT.render("One", 1, WHITE)  # Create hard label
        WIN.blit(one_label, (one_rect.x + 15, one_rect.y + 10))  # Display label in the middle

        pygame.draw.rect(WIN, WHITE, two_rect, 2 + borders[1])
        two_label = SMALL_TITLE_FONT.render("Two", 1, WHITE)  # Create hard label
        WIN.blit(two_label, (two_rect.x + 15, two_rect.y + 10))  # Display label in the middle

        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, num_of_players
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    return True, num_of_players
                if one_rect.collidepoint(event.pos):
                    borders = [3, 0]
                    num_of_players = 1
                if two_rect.collidepoint(event.pos):
                    borders = [0, 3]
                    num_of_players = 2
