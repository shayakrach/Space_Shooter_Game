# import pygame

from Laser import *


class Ship:
    cool_down_time = 30  # The minimum time between shoots

    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.health = 100
        self.ship_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (int(self.x), int(self.y)))

    def cool_down(self):
        # The player can shoot after half a second
        if self.cool_down_counter >= self.cool_down_time:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def get_vel(self):
        return self.vel
