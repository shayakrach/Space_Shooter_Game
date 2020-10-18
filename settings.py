import pygame
import os

WHITE = (255, 255, 255)

TITLE = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)

pygame.font.init()
TITLE_FONT = pygame.font.Font(os.path.join('fonts', 'FreshLychee-mLoK2.ttf'), 45)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)



def main(num_of_players):
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

    def draw_rect(rect, text, font, border, fix_x, fix_y, color=WHITE):
        pygame.draw.rect(WIN, color, rect, border)
        label = font.render(text, 1, color)  # Create hard label
        WIN.blit(label, (rect.x + fix_x, rect.y + fix_y))  # Display label in the middle

    def mid_width(obj):
        return int(WIDTH / 2 - obj.get_width() / 2)

    rect_width = 90
    rect_height = 40

    menu_rect = pygame.Rect(50, 50, 120, 60)
    one_rect = pygame.Rect(int(WIDTH / 2) - 100, 250, rect_width, rect_height)
    two_rect = pygame.Rect(int(WIDTH / 2) - 100 + rect_width, 250, rect_width, rect_height)

    up_rect = pygame.Rect(int(WIDTH / 2), int(HEIGHT / 2 + 140), 50, 50)
    down_rect = pygame.Rect(int(WIDTH / 2), int(HEIGHT / 2 + 200), 50, 50)
    right_rect = pygame.Rect(int(WIDTH / 2 + 60), int(HEIGHT / 2 + 200), 50, 50)
    left_rect = pygame.Rect(int(WIDTH / 2 - 60), int(HEIGHT / 2 + 200), 50, 50)
    shoot_rect = pygame.Rect(int(WIDTH / 2 - 60), int(HEIGHT / 2 + 260), 170, 50)

    hard_color = (255, 0, 0)
    normal_color = (255, 189, 34)
    easy_color = (80, 245, 68)

    up_bar_color = (163, 128, 222)
    pygame.draw.rect(WIN, up_bar_color, menu_rect, 2)

    borders = [3, 0] if num_of_players == 1 else [0, 3]

    while True:
        WIN.blit(BG, (0, 0))  # Display background

        settings_label = TITLE.render("SETTINGS", 1, WHITE)  # Create begin label
        WIN.blit(settings_label, (int(WIDTH / 2 - settings_label.get_width() / 2), 80))  # Display label in the middle

        draw_rect(menu_rect, 'menu', SMALL_TITLE_FONT, 2, 25, 20, up_bar_color)

        num_players_label = TITLE_FONT.render("Num of players", 1, WHITE)  # Create begin label
        WIN.blit(num_players_label, (mid_width(num_players_label), one_rect.y - 80))  # Display label in the middle

        draw_rect(one_rect, 'One', SMALL_TITLE_FONT, 2 + borders[0], 15, 10)
        draw_rect(two_rect, 'Two', SMALL_TITLE_FONT, 2 + borders[1], 15, 10)

        player1_label = TITLE_FONT.render("Player 1", 1, WHITE)  # Create begin label
        WIN.blit(player1_label, (mid_width(player1_label), one_rect.y + 80))  # Display label in the middle

        draw_rect(up_rect, 'up', SMALL_TITLE_FONT, 2, 15, 10)
        draw_rect(down_rect, 'do', SMALL_TITLE_FONT, 2, 15, 10)
        draw_rect(left_rect, 'le', SMALL_TITLE_FONT, 2, 15, 10)
        draw_rect(right_rect, 'ri', SMALL_TITLE_FONT, 2, 15, 10)
        draw_rect(shoot_rect, 'sp', SMALL_TITLE_FONT, 2, 15, 10)




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
