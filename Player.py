# import pygame
# import os

from Ship import *

SHIP = {
    'yellow': {
        'img' : pygame.image.load(os.path.join('assets', 'yellow_ship.png')),
        'laser_type' : 'yellow_laser'
    },
    'white': {
        'img' : pygame.image.load(os.path.join('assets', 'white_ship.png')),
        'laser_type': 'white_laser'
    }
}

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Player(Ship):

    def __init__(self, x, y, vel, color):
        super().__init__(x, y, vel)
        self.color = color
        self.ship_img = SHIP[color]['img']
        self.laser_type = SHIP[color]['laser_type']
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = self.health
        self.shooter_type = 'single_shooter'

    # Override 'move_lasers' function from the super class
    def move_lasers(self, objs, max_height, dead_objs=None):
        self.cool_down()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(max_height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if dead_objs is not None:
                            dead_objs.append(obj)
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # Override 'draw' function from the super class
    def draw(self, window):
        super().draw(window)
        for laser in self.lasers:
            laser.draw(window)
        self.health_bar(window)

    # Represent the mount health of the player
    def health_bar(self, window):
        red_rect = (self.x + 10, self.y + self.ship_img.get_height() - 15, self.ship_img.get_width() - 18, 10)
        pygame.draw.rect(window, RED, red_rect)
        part_of_health = (self.ship_img.get_width() - 18) * (self.health / self.max_health)
        if part_of_health > 0:
            green_rect = (self.x + 10, self.y + self.ship_img.get_height() - 15, part_of_health, 10)
            pygame.draw.rect(window, GREEN, green_rect)

    def shoot(self):
        if self.cool_down_counter == 0:
            err = (12 if 'arrow' in self.laser_type else 0)
            if self.shooter_type == 'double_shooter':
                laser = Laser(self.x + 55 + err, self.y, self.laser_type)
                self.lasers.append(laser)
                laser = Laser(self.x - 15 + err, self.y, self.laser_type)
                self.lasers.append(laser)
            else:
                if self.shooter_type == 'triple_shooter':
                    laser = Laser(self.x + 60 + err, self.y, self.laser_type + '_plus30')
                    self.lasers.append(laser)
                    laser = Laser(self.x - 20 + err, self.y, self.laser_type + '_minus30')
                    self.lasers.append(laser)
                laser = Laser(self.x + 20 + err, self.y - 20, self.laser_type)
                self.lasers.append(laser)
            self.cool_down_counter = 1

    def increase_health(self):
        self.health = min(self.max_health, self.health + 40)

    def get_shooter(self):
        return self.shooter_type

    def change_shooter(self, shooter_type):
        self.shooter_type = shooter_type

    def change_laser(self, laser_type):
        self.laser_type = laser_type

    def change_vel(self, vel):
        self.vel = vel

    def change_to_automate(self):
        self.cool_down_time = 15

    def reset_cool_down_timer(self):
        self.cool_down_time = 30
