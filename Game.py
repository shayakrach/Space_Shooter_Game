# import pygame
# import os
# import random

# from Laser import *
# from Ship import *
from Player import *
from Enemy import *
from Gift import *

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
FPS = 70  # frames per second

# Load windows game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
PLAYER_POSITION_X, PLAYER_POSITION_Y = WIDTH / 2 - 50, HEIGHT - 120

# Sensitive of the press keys for each movement
PLAYER_VEL = 5

# Set the name on the upper part of the window
pygame.display.set_caption("Space Shooter Game")

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

# Small icons
LIFE = pygame.image.load(os.path.join('assets', 'heart.png'))
DOUBLE_SHOOTER = pygame.image.load(os.path.join('assets', 'double_shooter_small_icon.png'))
TRIPLE_SHOOTER = pygame.image.load(os.path.join('assets', 'triple_shooter_small_icon.png'))
MORE_SPEED = pygame.image.load(os.path.join('assets', 'more_speed_small_icon.png'))
YELLOW_ARROW = pygame.image.load(os.path.join('assets', 'yellow_arrow_small_icon.png'))
AUTOMATIC = pygame.image.load(os.path.join('assets', 'automatic_small.icon.png'))



# Types of fonts
MAIN_FONT = pygame.font.SysFont('comicsans', 50)
LOST_FONT = pygame.font.SysFont('comicsans', 60)
LEVEL_FONT = pygame.font.Font(os.path.join('fonts', 'gomarice_game_continue_02.ttf'), 65)
LARGE_FONT = pygame.font.SysFont('comicsans', 75)
SMALL_FONT = pygame.font.SysFont('comicsans', 35)

GIFT_MAP = {
    "double_shooter": DOUBLE_SHOOTER,
    "triple_shooter": TRIPLE_SHOOTER,
    "more_speed": MORE_SPEED,
    "yellow_arrow": YELLOW_ARROW,
    'automatic': AUTOMATIC
}

DIF_MAP = {
    "hard": 9,
    "normal": 5,
    "easy": 1
}

def start(user_name, mode):
    # Make the game stays consistent on any device
    clock = pygame.time.Clock()

    dif = DIF_MAP[mode]
    run = True
    just_begin = True
    Scroll_bg = 0
    begin_count = 0

    level = 0  # player start level
    lives = 5  # player start lives

    gifts = []
    player_gifts = []
    automatic_level = 0

    # Set the number and velocity of the enemies
    enemies = []
    dead_enemies = []
    wave_length = int(dif/2 + 3)
    enemy_vel = 0.9 + (dif/100)

    # Make player instance start in position
    player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_VEL)

    lost = False
    level_up = False

    # The number of times (the number of seconds) the text will remain on the screen
    lost_count = 0
    level_count = 0

    def activate_player():

        # Pressed keys
        left_key = pygame.K_LEFT
        right_key = pygame.K_RIGHT
        up_key = pygame.K_UP
        down_key = pygame.K_DOWN
        shoot_key = pygame.K_SPACE

        # Control the pressed keys
        keys = pygame.key.get_pressed()

        # Change the position of the ship without crossing the corners
        if keys[left_key]:  # move left
            if player.x - player.get_vel() > -10:
                player.x -= player.get_vel()
            else:
                player.x = -10
        if keys[right_key]:  # move right
            if player.x + player.get_vel() + player.get_width() - 10 < WIDTH:
                player.x += player.get_vel()
            else:
                player.x = WIDTH - player.get_width() + 10
        if keys[up_key]:  # move up
            if player.y - player.get_vel() > -10:
                player.y -= player.get_vel()
            else:
                player.y = -10
        if keys[down_key]:  # move down
            if player.y + player.get_vel() + player.get_height() - 20 < HEIGHT:
                player.y += player.get_vel()
            else:
                player.y = HEIGHT - player.get_height() + 20
        if keys[shoot_key]:  # shoot
            player.shoot()

    def activate_enemies():
        nonlocal lives, player_gifts, dif

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_lasers(player, HEIGHT)

            # Set probability this enemy will shoot on the player depend on the difficulty
            if random.randrange(0, int(3 * FPS / (1 + dif/30))) == 1:
                enemy.shoot()

            # The enemy collided with the player
            if collide(enemy, player):
                player.health = max(player.health - 20, 0)
                dead_enemies.append(enemy)
                enemies.remove(enemy)

            # The player missed the enemy
            elif enemy.get_y_pos() + enemy.get_height() > HEIGHT:
                lives -= 1
                player.change_shooter('single_shooter')
                player.change_laser('yellow_laser')
                player.change_vel(PLAYER_VEL)
                player_gifts = []
                enemies.remove(enemy)
                player.reset_cool_down_timer()

    def activate_lasers():
        # Activate all the lasers of the player
        player.move_lasers(enemies, HEIGHT, dead_enemies)

        for enemy in dead_enemies[:]:
            enemy.move_lasers(player, HEIGHT)

    def activate_gifts():
        nonlocal lives, automatic_level

        for gift in gifts[:]:
            gift.move()
            if collide(gift, player):
                if gift.get_type() == 'health':
                    player.increase_health()
                elif gift.get_type() == 'life':
                    lives += 1
                elif gift.get_type() == 'more_shooter':
                    if player.get_shooter() == 'single_shooter':
                        player.change_shooter('double_shooter')
                    elif player.get_shooter() == 'double_shooter':
                        player_gifts.remove('double_shooter')
                        player.change_shooter('triple_shooter')
                    if player.get_shooter() not in player_gifts:
                        player_gifts.append(player.get_shooter())
                else:
                    if gift.get_type() == 'more_speed':
                        player.change_vel(8)
                    if gift.get_type() == 'yellow_arrow':
                        player.change_laser('yellow_arrow')
                    if gift.get_type() == 'automatic':
                        player.change_to_automate()
                        automatic_level = level
                    if gift.get_type() not in player_gifts:
                        player_gifts.append(gift.get_type())

                gifts.remove(gift)

            elif gift.get_y_pos() + gift.get_height() > HEIGHT:
                gifts.remove(gift)

    def activate_new_level():
        nonlocal level, wave_length, enemy_vel, lives, level_up, level_count, dif
        level += 1
        wave_length += 1 + int(dif/2)
        # increase enemy velocity every level till some limit, depend on the difficulty
        enemy_vel = min(enemy_vel + (enemy_vel * (0.1 / level)), 1.5 + (dif/20))

        # After every 5 levels the player get extra lives and health
        if level % 5 == 0:
            lives = min(10, lives + 1)
            player.increase_health()

        if 'automatic' in player_gifts and level - automatic_level > 2:
            player_gifts.remove('automatic')
            player.reset_cool_down_timer()


        # Reset the counter time of level label
        level_up = True
        level_count = 0

        # Create a new, better and more enemies for the next level
        for i in range(wave_length):
            enemy_random_pos_x = random.randrange(30, WIDTH - 80)
            if level == 1:
                # More time for the player to read the instructions
                enemy_random_pos_y = random.randrange(-1800, -700 - 20*dif)
            else:
                enemy_random_pos_y = random.randrange(max(-2500, -1500 - (level * (50 + dif))), - 100)
            random_color = random.choice(['red', 'blue', 'green'])

            rnd_factor = random.uniform(0.8, 1 + (dif/25))
            enemy = Enemy(enemy_random_pos_x, enemy_random_pos_y, random_color, enemy_vel * rnd_factor)
            enemies.append(enemy)

        random_gift = random.choice(['automatic','yellow_arrow', 'more_speed', 'more_shooter', 'health', 'life'])
        gift_random_pos_x = random.randrange(30, WIDTH - 80)
        gift_random_pos_y = random.randrange(-1500, -400)
        gift = Gift(gift_random_pos_x, gift_random_pos_y, enemy_vel, random_gift)
        gifts.append(gift)

    def redraw_window(y):
        # Display background
        rel_y = y % HEIGHT
        WIN.blit(BG, (0, rel_y))
        WIN.blit(BG, (0, rel_y - HEIGHT))

        # draw enemies
        for enemy in enemies:
            enemy.draw(WIN)

        for enemy in dead_enemies[:]:
            if len(enemy.lasers) == 0:
                dead_enemies.remove(enemy)
            else:
                enemy.draw_lasers(WIN)

        for gift in gifts:
            gift.draw(WIN)

        # draw player
        player.draw(WIN)
        if just_begin:
            level_label = LARGE_FONT.render("Good luck {}".format(user_name), 1, WHITE)  # Create level label
            middle_of_screen = int(WIDTH / 2 - level_label.get_width() / 2)
            WIN.blit(level_label, (middle_of_screen, int(HEIGHT / 2 - 150)))  # Display label in the middle

            dif_label = SMALL_FONT.render("Mode: {}".format(mode), 1, WHITE)  # Create difficulty label
            middle_of_screen = int(WIDTH / 2 - dif_label.get_width() / 2)
            WIN.blit(dif_label, (middle_of_screen, int(HEIGHT / 2 + 50)))  # Display label in the middle

            ins_label = SMALL_FONT.render("Use the arrows to move and space to shoot", 1, WHITE)  # Create instructions label
            middle_of_screen = int(WIDTH / 2 - ins_label.get_width() / 2)
            WIN.blit(ins_label, (middle_of_screen, int(HEIGHT / 2 +100)))  # Display label in the middle

        # Display the current level on the screen
        elif level_up:
            level_label = LEVEL_FONT.render("Level {}".format(level), 1, WHITE)  # Create level label
            middle_of_screen = int(WIDTH / 2 - level_label.get_width() / 2)
            WIN.blit(level_label, (middle_of_screen, int(HEIGHT / 2 - 50)))  # Display label in the middle

        # Display the 'You Lost!!' on the screen
        if lost:
            lost_label = LOST_FONT.render("You Lost!!", 1, WHITE)  # Create 'You Lost!!' label
            middle_of_screen = int(WIDTH / 2 - lost_label.get_width() / 2)
            WIN.blit(lost_label, (middle_of_screen, int(HEIGHT / 2 - 50)))  # Display label in the middle

        # draw hearts represents player life
        for life in range(lives):
            WIN.blit(LIFE, (LIFE.get_width() * life, 0))

        for i, gift in enumerate(player_gifts[:]):
            WIN.blit(GIFT_MAP[gift], (WIDTH - 50 * (i + 1), 0))

        # Refresh the display
        pygame.display.update()

    while run:
        clock.tick(FPS)  # Run for <FPS> frames per second
        redraw_window(Scroll_bg)  # Draw window
        if just_begin:
            if begin_count > FPS * 4.5:
                just_begin = False
            else:
                begin_count += 1
                Scroll_bg +=2
        else:
            # Check if the player lost
            if lives <= 0 or player.health <= 0:
                lost = True
                lost_count += 1

            # Keep showing "You Lost!!" text on the screen for 3 seconds
            if lost:
                if lost_count > FPS * 2.5:
                    run = False
                else:
                    continue

        # Create Next level after the player defeat all the enemies
        if len(enemies) == 0 and lives != 0:
            activate_new_level()

        # Keep showing "Level <level>" text on the screen for 2 seconds while after thw player finished the last one
        if level_up:
            seconds = 3.5
            # scrolling after no enemy laser on the screen
            if level % 5 == 0 and len(dead_enemies) == 0:
                seconds = 6
                Scroll_bg += 5

            if level_count > FPS * seconds:
                level_up = False
            else:
                level_count += 1

        # Activate all the enemies in this level
        else:
            activate_enemies()

        # Activate player movement
        activate_player()

        # Activate all lasers
        activate_lasers()

        # Activate all the remain gifts
        activate_gifts()

        # Close the game when clicking the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0

    # Calculate player score
    mount_of_left_enemies = min(len(enemies) + 5 - lives, wave_length)
    part_of_killed_enemies = 1 - (mount_of_left_enemies / wave_length)
    score = round(level + part_of_killed_enemies - 1, 2)
    return score
