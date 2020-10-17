# import pygame
# import os

from Ship import *

# Ships images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'red_ship.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'green_ship.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'blue_ship.png'))

# Lasers images
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, 'red_laser'),
        "green": (GREEN_SPACE_SHIP, 'green_laser'),
        "blue": (BLUE_SPACE_SHIP, 'blue_laser')
    }

    def __init__(self, x, y, color, vel=1.0):
        super().__init__(x, y, vel)
        self.color = color
        self.ship_img, self.laser_type = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = self.health

    def move(self):
        self.y += self.vel

    # Override 'shoot' function from the super class to fix blue ship shoot
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 7, self.y, self.laser_type)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        window.blit(self.ship_img, (int(self.x), int(self.y)))
        for laser in self.lasers:
            laser.draw(window)

    def draw_lasers(self, window):
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, objs, max_height):
        self.cool_down()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(max_height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health = max(obj.health - 10, 0)
                        self.lasers.remove(laser)
                        break
