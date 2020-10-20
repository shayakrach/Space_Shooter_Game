import pygame
import os

WHITE = (255, 255, 255)

rect = {}

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))
middle_width = int(WIDTH / 2)
middle_height = int(HEIGHT / 2)

pygame.font.init()
TITLE = pygame.font.Font(os.path.join('fonts', 'ARCADE.TTF'), 100)
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
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_LEFT: '<-',
    pygame.K_RIGHT: '->',
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'do',
    pygame.K_SPACE: 'sp'
}


def main(num_of_players, player_keys):
    def key_rect_pos(flip, error=0):
        return 470 + error + flip * (num_of_players - 1) * 230

    rect_width = 90
    rect_height = 40

    menu_rect = pygame.Rect(50, 50, 120, 60)
    one_rect = pygame.Rect(middle_width - 100, 250, rect_width, rect_height)
    two_rect = pygame.Rect(middle_width - 100 + rect_width, 250, rect_width, rect_height)

    up_bar_color = (163, 128, 222)

    participants_borders = [3, 0] if num_of_players == 1 else [0, 3]
    run = None

    borders = {
        0: {
            'left': 2,
            'right': 2,
            'up': 2,
            'down': 2,
            'shoot': 2,
        },
        1: {
            'left': 2,
            'right': 2,
            'up': 2,
            'down': 2,
            'shoot': 2,
        }
    }

    def change_key(key, i):
        borders[i][key] = 5
        while True:
            draw_settings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    borders[i][key] = 2
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_rect.collidepoint(event.pos):
                        borders[i][key] = 2
                        return True
                    if rect[i][key].collidepoint(event.pos):
                        borders[i][key] = 2
                        return None
                if event.type == pygame.KEYDOWN:
                    try:
                        if event.key not in player_keys[i].values() and event.key in KEYS.keys():
                            player_keys[i][key] = event.key
                    finally:
                        borders[i][key] = 2
                        return None

    def draw_rect(rect, text, font, border, fix_x, fix_y, color=WHITE):
        pygame.draw.rect(WIN, color, rect, border)
        label = font.render(text, 1, color)  # Create hard label
        WIN.blit(label, (rect.x + fix_x, rect.y + fix_y))  # Display label in the middle

    def mid_width(obj):
        return int(WIDTH / 2 - obj.get_width() / 2)

    def draw_settings():
        global rect

        rect = {
            0: {
                'up': pygame.Rect(key_rect_pos(-1), middle_height + 140, 50, 50),
                'down': pygame.Rect(key_rect_pos(-1), middle_height + 200, 50, 50),
                'right': pygame.Rect(key_rect_pos(-1, 60), middle_height + 200, 50, 50),
                'left': pygame.Rect(key_rect_pos(-1, -60), middle_height + 200, 50, 50),
                'shoot': pygame.Rect(key_rect_pos(-1, -60), middle_height + 260, 170, 50)
            },
            1: {
                'up': pygame.Rect(key_rect_pos(1), middle_height + 140, 50, 50),
                'down': pygame.Rect(key_rect_pos(1), middle_height + 200, 50, 50),
                'right': pygame.Rect(key_rect_pos(1, 60), middle_height + 200, 50, 50),
                'left': pygame.Rect(key_rect_pos(1, -60), middle_height + 200, 50, 50),
                'shoot': pygame.Rect(key_rect_pos(1, -60), middle_height + 260, 170, 50)
            }
        }

        WIN.blit(BG, (0, 0))  # Display background

        settings_label = TITLE.render("SETTINGS", 1, WHITE)  # Create begin label
        WIN.blit(settings_label, (mid_width(settings_label), 80))  # Display label in the middle

        draw_rect(menu_rect, 'menu', SMALL_TITLE_FONT, 2, 25, 20, up_bar_color)

        num_players_label = TITLE_FONT.render("Num of players", 1, WHITE)  # Create begin label
        WIN.blit(num_players_label, (mid_width(num_players_label), one_rect.y - 80))  # Display label in the middle

        draw_rect(one_rect, 'One', SMALL_TITLE_FONT, 2 + participants_borders[0], 15, 10)
        draw_rect(two_rect, 'Two', SMALL_TITLE_FONT, 2 + participants_borders[1], 15, 10)

        for i in range(num_of_players):
            player1_label = TITLE_FONT.render("Player {}".format(i + 1), 1, WHITE)  # Create begin label
            label_x_pos = mid_width(player1_label) + (i * 2 - 1) * (num_of_players - 1) * 230
            WIN.blit(player1_label, (label_x_pos, one_rect.y + 80))  # Display label in the middle

            draw_rect(rect[i]['up'], KEYS[player_keys[i]['up']], SMALL_TITLE_FONT, borders[i]['up'], 15, 10)
            draw_rect(rect[i]['down'], KEYS[player_keys[i]['down']], SMALL_TITLE_FONT, borders[i]['down'], 15, 10)
            draw_rect(rect[i]['left'], KEYS[player_keys[i]['left']], SMALL_TITLE_FONT, borders[i]['left'], 15, 10)
            draw_rect(rect[i]['right'], KEYS[player_keys[i]['right']], SMALL_TITLE_FONT, borders[i]['right'], 15, 10)
            draw_rect(rect[i]['shoot'], KEYS[player_keys[i]['shoot']], SMALL_TITLE_FONT, borders[i]['shoot'], 75, 10)

        # Refresh the display
        pygame.display.update()

    while run is None:
        draw_settings()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    run = True
                if one_rect.collidepoint(event.pos):
                    participants_borders = [3, 0]
                    num_of_players = 1
                if two_rect.collidepoint(event.pos):
                    participants_borders = [0, 3]
                    num_of_players = 2
                for i in range(num_of_players):
                    if rect[i]['up'].collidepoint(event.pos):
                        run = change_key('up', i)
                    if rect[i]['down'].collidepoint(event.pos):
                        run = change_key('down', i)
                    if rect[i]['left'].collidepoint(event.pos):
                        run = change_key('left', i)
                    if rect[i]['right'].collidepoint(event.pos):
                        run = change_key('right', i)
                    if rect[i]['shoot'].collidepoint(event.pos):
                        run = change_key('shoot', i)

    return run, num_of_players, player_keys
