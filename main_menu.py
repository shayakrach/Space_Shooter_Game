import pygame
import Game
import os

WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

pygame.font.init()
TITLE_FONT = pygame.font.SysFont('ariel', 65)
SMALL_TITLE_FONT = pygame.font.SysFont('ariel', 30)


def main_menu():
    run = True
    record = 0
    is_new_record = False
    current_score_label = None

    while run:
        WIN.blit(BG, (0, 0))  # Display background
        middle_height = int(HEIGHT / 2 - 50)

        # Labels
        broke_record_label = TITLE_FONT.render("Your broke the record!!", 1, WHITE)  # Create record label
        record_label = TITLE_FONT.render("Your record: {:.2f}".format(record), 1, WHITE)  # Create record label
        begin_game_label = TITLE_FONT.render("Press the mouse to begin...", 1, WHITE)  # Create begin label

        if is_new_record:
            middle_width = int(WIDTH / 2 - broke_record_label.get_width() / 2)
            WIN.blit(broke_record_label, (middle_width, middle_height - 150))  # Display label in the middle

        if record > 0:
            middle_width = int(WIDTH / 2 - record_label.get_width() / 2)
            WIN.blit(record_label, (middle_width, middle_height - 100))  # Display label in the middle

        if current_score_label is not None:
            middle_width = int(WIDTH / 2 - current_score_label.get_width() / 2)
            WIN.blit(current_score_label, (middle_width, HEIGHT - 70))  # Display label in the middle

        middle_width = int(WIDTH / 2 - begin_game_label.get_width() / 2)
        WIN.blit(begin_game_label, (middle_width, middle_height))  # Display label in the middle

        # Refresh the display
        pygame.display.update()
        # Start the game by moving the mouse or get out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_record = Game.start()
                # Create current score label
                current_score_label = SMALL_TITLE_FONT.render("current score: {:.2f}".format(new_record), 1, WHITE)

                is_new_record = new_record > record
                record = max(record, new_record)

    pygame.quit()


main_menu()
