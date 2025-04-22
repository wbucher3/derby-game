import pygame
import math
import random
from util import scale_image

class Horse:
    def __init__(self, 
                name,
                max_velocity, 
                luck,
                predictablity,
                rotation_velocity,
                acceleration,
                start_position
                ):
        self.img = scale_image(pygame.image.load("imgs/" + name + ".png"), 0.8)
        self.max_velocity = max_velocity
        self.luck = luck
        self.predictablity = predictablity
        self.rotation_velocity = rotation_velocity
        self.acceleration = acceleration
        self.velocity = 0
        self.angle = random.randint(0, 360)
        self.x, self.y = start_position
        self.start_position = start_position

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        self.y -= vertical
        self.x -= horizontal

    def bounce(self):
        random_direction = random.randint(0, 360)
        self.angle = random_direction
        self.move()

    def collide(self, mask, x=0, y=0):
        horse_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(horse_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.start_position
        self.angle = 0
        self.velocity = 0