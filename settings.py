import pygame
import os

WHITE = (255, 255, 255)

TITLE = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)

pygame.font.init()
TITLE_FONT = pygame.font.Font(os.path.join('fonts', 'FreshLychee-mLoK2.ttf'), 45)
NAME_FONT = pygame.font.Font(None, 55)
SMALL_TITLE_FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)

KEYS = {
    pygame.K_a: 'a',
    pygame.K_b: 'b',
    pygame.K_c: 'c',
    pygame.K_d: 'd',
    pygame.K_e: 'e',
    pygame.K_f: 'f',
    pygame.K_g: 'g',
    pygame.K_h: 'h',
    pygame.K_i: 'i',
    pygame.K_j: 'j',
    pygame.K_k: 'k',
    pygame.K_l: 'l',
    pygame.K_m: 'm',
    pygame.K_n: 'n',
    pygame.K_o: 'o',
    pygame.K_p: 'p',
    pygame.K_q: 'q',
    pygame.K_r: 'r',
    pygame.K_s: 's',
    pygame.K_t: 't',
    pygame.K_u: 'u',
    pygame.K_v: 'v',
    pygame.K_w: 'w',
    pygame.K_x: 'x',
    pygame.K_y: 'y',
    pygame.K_z: 'z',
    pygame.K_LEFT: 'le',
    pygame.K_RIGHT: 'ri',
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'do',
    pygame.K_SPACE: 'sp'
}


def main(num_of_players):
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))
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

    up_bar_color = (163, 128, 222)

    participants_borders = [3, 0] if num_of_players == 1 else [0, 3]
    keys_borders = [0, 0, 0, 0, 0]
    exit = None

    player1_keys = {
        'left_key': 'a',
        'right_key': 'b',
        'up_key': 'c',
        'down_key': 'd',
        'shoot_key': 'e'
    }

    def change_key(key,rect):
        while True:
            draw_settings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_rect.collidepoint(event.pos):
                        return True
                    if rect.collidepoint(event.pos):
                        return None
                if event.type == pygame.KEYDOWN:
                    player1_keys[key] = KEYS[event.key]
                    return None

    def draw_rect(rect, text, font, border, fix_x, fix_y, color=WHITE):
        pygame.draw.rect(WIN, color, rect, border)
        label = font.render(text, 1, color)  # Create hard label
        WIN.blit(label, (rect.x + fix_x, rect.y + fix_y))  # Display label in the middle

    def mid_width(obj):
        return int(WIDTH / 2 - obj.get_width() / 2)

    def draw_settings():
        WIN.blit(BG, (0, 0))  # Display background

        settings_label = TITLE.render("SETTINGS", 1, WHITE)  # Create begin label
        WIN.blit(settings_label, (int(WIDTH / 2 - settings_label.get_width() / 2), 80))  # Display label in the middle

        draw_rect(menu_rect, 'menu', SMALL_TITLE_FONT, 2, 25, 20, up_bar_color)

        num_players_label = TITLE_FONT.render("Num of players", 1, WHITE)  # Create begin label
        WIN.blit(num_players_label, (mid_width(num_players_label), one_rect.y - 80))  # Display label in the middle

        draw_rect(one_rect, 'One', SMALL_TITLE_FONT, 2 + participants_borders[0], 15, 10)
        draw_rect(two_rect, 'Two', SMALL_TITLE_FONT, 2 + participants_borders[1], 15, 10)

        player1_label = TITLE_FONT.render("Player 1", 1, WHITE)  # Create begin label
        WIN.blit(player1_label, (mid_width(player1_label), one_rect.y + 80))  # Display label in the middle

        draw_rect(up_rect, player1_keys['up_key'], SMALL_TITLE_FONT, 2+ keys_borders[0], 15+keys_borders[0], 10)
        draw_rect(down_rect, player1_keys['down_key'], SMALL_TITLE_FONT, 2 + keys_borders[1], 15, 10)
        draw_rect(left_rect, player1_keys['left_key'], SMALL_TITLE_FONT, 2 + keys_borders[2], 15, 10)
        draw_rect(right_rect, player1_keys['right_key'], SMALL_TITLE_FONT, 2 + keys_borders[3], 15, 10)
        draw_rect(shoot_rect, player1_keys['shoot_key'], SMALL_TITLE_FONT, 2 + keys_borders[4], 15, 10)

        # Refresh the display
        pygame.display.update()


    while True:
        keys_borders = [0,0,0,0,0]
        draw_settings()

        # Start the game by moving the mouse or get out
        if exit is not None:
            return exit, num_of_players

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, num_of_players
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    return True, num_of_players
                if one_rect.collidepoint(event.pos):
                    participants_borders = [3, 0]
                    num_of_players = 1
                if two_rect.collidepoint(event.pos):
                    participants_borders = [0, 3]
                    num_of_players = 2
                if up_rect.collidepoint(event.pos):
                    keys_borders = [3, 0, 0, 0, 0]
                    exit = change_key('up_key', up_rect)
                if down_rect.collidepoint(event.pos):
                    keys_borders = [0, 3, 0, 0, 0]
                    exit = change_key('down_key', down_rect)
                if left_rect.collidepoint(event.pos):
                    keys_borders = [0, 0, 3, 0, 0]
                    exit = change_key('left_key', left_rect)
                if right_rect.collidepoint(event.pos):
                    keys_borders = [0, 0, 0, 3, 0]
                    exit = change_key('right_key', right_rect)
                if shoot_rect.collidepoint(event.pos):
                    keys_borders = [0, 0, 0, 0, 3]
                    exit = change_key('shoot_key', shoot_rect)
