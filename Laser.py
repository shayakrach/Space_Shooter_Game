import pygame
import os

# Lasers images
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
YELLOW_ARROW = pygame.image.load(os.path.join('assets', 'yellow_arrow.png'))


class Laser:
    GUN_MAP = {
        "red_laser": (RED_LASER, 3.5),
        "green_laser": (GREEN_LASER, 3.5),
        "blue_laser": (BLUE_LASER, 3.5),
        "yellow_laser": (YELLOW_LASER, -5),
        "yellow_arrow": (YELLOW_ARROW, -9)
    }

    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.type = typ
        self.img, self.vel = self.GUN_MAP[typ]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y)))

    def move(self):
        self.y += self.vel

    def off_screen(self, height):
        return self.y > height or self.y < -50

    def collision(self, obj):
        return collide(obj, self)


# Check if the 2 objects collided
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
