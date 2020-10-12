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
MORE_SPEED = pygame.image.load(os.path.join('assets', 'more_speed_small_icon.png'))
YELLOW_ARROW = pygame.image.load(os.path.join('assets', 'yellow_arrow_small_icon.png'))

# Types of fonts
MAIN_FONT = pygame.font.SysFont('comicsans', 50)
LOST_FONT = pygame.font.SysFont('comicsans', 60)
LEVEL_FONT = pygame.font.SysFont('comicsans', 65)

GIFT_MAP = {
    "double_shooter": DOUBLE_SHOOTER,
    "more_speed": MORE_SPEED,
    "yellow_arrow": YELLOW_ARROW
}


def start():
    run = True
    level = 0  # player start level
    lives = 5  # player start lives

    gifts = []
    player_gifts = []

    # Set the number and velocity of the enemies
    enemies = []
    dead_enemies = []
    wave_length = 2
    enemy_vel = 1

    # Make player instance start in position
    player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_VEL)

    # Make the game stays consistent on any device
    clock = pygame.time.Clock()

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
            if player.x - player.get_vel() > 0:
                player.x -= player.get_vel()
            else:
                player.x = 0
        if keys[right_key]:  # move right
            if player.x + player.get_vel() + player.get_width() < WIDTH:
                player.x += player.get_vel()
            else:
                player.x = WIDTH - player.get_width()
        if keys[up_key]:  # move up
            if player.y - player.get_vel() > 0:
                player.y -= player.get_vel()
            else:
                player.y = 0
        if keys[down_key]:  # move down
            if player.y + player.get_vel() + player.get_height() + 10 < HEIGHT:
                player.y += player.get_vel()
            else:
                player.y = HEIGHT - player.get_height()
        if keys[shoot_key]:  # shoot
            player.shoot()

        # Activate all the lasers of the player
        player.move_lasers(enemies, HEIGHT, dead_enemies)

    def activate_enemies():
        nonlocal lives, player_gifts

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_lasers(player, HEIGHT)

            # Set probability this enemy will shoot on the player
            if random.randrange(0, 3 * FPS) == 1:
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

        for enemy in dead_enemies[:]:
            enemy.move_lasers(player, HEIGHT)

    def activate_gifts():
        nonlocal lives

        for gift in gifts[:]:
            gift.move()
            if collide(gift, player):
                if gift.get_type() == 'health':
                    player.increase_health()
                elif gift.get_type() == 'life':
                    lives += 1
                else:
                    if gift.get_type() == 'double_shooter':
                        player.change_shooter('double_shooter')
                    if gift.get_type() == 'more_speed':
                        player.change_vel(8)
                    if gift.get_type() == 'yellow_arrow':
                        player.change_laser('yellow_arrow')
                    if gift.get_type() not in player_gifts:
                        player_gifts.append(gift.get_type())

                gifts.remove(gift)

            elif gift.get_y_pos() + gift.get_height() > HEIGHT:
                gifts.remove(gift)

    def activate_new_level():
        nonlocal level, wave_length, enemy_vel, lives, level_up, level_count
        level += 1
        wave_length += 3
        enemy_vel = min(enemy_vel + (enemy_vel * (0.1 / level)), 1.6)  # increase enemy velocity every level till 1.6

        # After every 5 levels the player get extra lives and health
        if level % 5 == 0:
            lives = min(10, lives + 1)
            player.increase_health()

        # Reset the counter time of level label
        level_up = True
        level_count = 0

        # Create a new, better and more enemies for the next level
        for i in range(wave_length):
            enemy_random_pos_x = random.randrange(30, WIDTH - 80)
            enemy_random_pos_y = random.randrange(max(-2500, -1500 - (level * 50)), -100)
            random_color = random.choice(['red', 'blue', 'green'])

            rnd_factor = random.uniform(0.8, 1.2)
            enemy = Enemy(enemy_random_pos_x, enemy_random_pos_y, random_color, enemy_vel * rnd_factor)
            enemies.append(enemy)

        random_gift = random.choice(['health', 'life', 'double_shooter', 'more_speed', 'yellow_arrow'])
        gift_random_pos_x = random.randrange(30, WIDTH - 80)
        gift_random_pos_y = random.randrange(-1200, -200)
        gift = Gift(gift_random_pos_x, gift_random_pos_y, enemy_vel, random_gift)
        gifts.append(gift)

    def redraw_window():
        # Display background
        WIN.blit(BG, (0, 0))

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

        # Display the current level on the screen
        if level_up:
            level_label = LEVEL_FONT.render("level {}".format(level), 1, WHITE)  # Create level label
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
        redraw_window()  # Draw window

        # Check if the player lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        # Keep showing "You Lost!!" text on the screen for 3 seconds
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # Create Next level after the player defeat all the enemies
        if len(enemies) == 0 and lives != 0:
            activate_new_level()

        # Keep showing "Level <level>" text on the screen for 2 seconds while after thw player finished the last one
        if level_up:
            if level_count > FPS * 2.5:
                level_up = False
            else:
                level_count += 1

        # Close the game when clicking the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Activate player movement and shooting
        activate_player()

        # Activate all the enemies in this level
        activate_enemies()

        # Activate all the remain gifts
        activate_gifts()

    # Calculate player score
    mount_of_left_enemies = min(len(enemies) + 5 - lives, wave_length)
    part_of_killed_enemies = 1 - (mount_of_left_enemies / wave_length)
    return level + part_of_killed_enemies
