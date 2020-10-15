import pygame
import os

# Lasers images
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
YELLOW_LASER_PLUS30 = pygame.image.load(os.path.join('assets', '30_yellow_laser.png'))
YELLOW_LASER_MINUS30 = pygame.image.load(os.path.join('assets', '-30_yellow_laser.png'))
YELLOW_ARROW = pygame.image.load(os.path.join('assets', 'yellow_arrow.png'))
YELLOW_ARROW_PLUS30 = pygame.image.load(os.path.join('assets', '30_yellow_arrow.png'))
YELLOW_ARROW_MINUS30 = pygame.image.load(os.path.join('assets', '-30_yellow_arrow.png'))


class Laser:
    GUN_MAP = {
        "red_laser": (RED_LASER, 0, 3.5),
        "green_laser": (GREEN_LASER, 0, 3.5),
        "blue_laser": (BLUE_LASER, 0, 3.5),
        "yellow_laser": (YELLOW_LASER,0, -5),
        "yellow_laser_plus30": (YELLOW_LASER_PLUS30, 2.9, -5),
        "yellow_laser_minus30": (YELLOW_LASER_MINUS30, -2.9, -5),
        "yellow_arrow": (YELLOW_ARROW, 0, -9),
        "yellow_arrow_plus30": (YELLOW_ARROW_PLUS30, 5.2, -9),
        "yellow_arrow_minus30": (YELLOW_ARROW_MINUS30, -5.2, -9),
    }

    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.type = typ
        self.img, self.vel_x, self.vel_y = self.GUN_MAP[typ]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y)))

    def move(self):
        self.y += self.vel_y
        self.x += self.vel_x

    def off_screen(self, height):
        return self.y > height or self.y < -50

    def collision(self, obj):
        return collide(obj, self)


# Check if the 2 objects collided
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
