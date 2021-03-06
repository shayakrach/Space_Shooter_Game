import pygame
import os
import random

HEALTH = pygame.image.load(os.path.join('assets', 'health.png'))
LIFE = pygame.image.load(os.path.join('assets', 'medium_heart.png'))
MORE_SHOOTER = pygame.image.load(os.path.join('assets', 'more_shooter.png'))
QUESTION_MARK = pygame.image.load(os.path.join('assets', 'question_mark.png'))
MORE_SPEED = pygame.image.load(os.path.join('assets', 'more_speed.png'))
YELLOW_ARROW = pygame.image.load(os.path.join('assets', 'yellow_arrow.png'))
AUTOMATIC = pygame.image.load(os.path.join('assets', 'automatic.png'))


class Gift:
    GIFT_MAP = {
        "health": HEALTH,
        "life": LIFE,
        "more_shooter": MORE_SHOOTER,
        "more_speed": MORE_SPEED,
        "arrow": YELLOW_ARROW,
        "automatic": AUTOMATIC
    }

    def __init__(self, x, y, vel, typ):
        self.x = x
        self.y = y
        self.vel = vel
        self.type = typ
        if random.randrange(len(self.GIFT_MAP)) == 0:
            self.img = QUESTION_MARK
        else:
            self.img = self.GIFT_MAP[self.type]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y)))

    def move(self):
        self.y += self.vel

    def collision(self, obj):
        return collide(obj, self)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.x

    def get_type(self):
        return self.type

    def get_img(self):
        return self.img


# Check if the 2 objects collided
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
