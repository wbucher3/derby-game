import pygame
import math
import random
from util import scale_image

class Horse(pygame.sprite.Sprite):
    def __init__(self, 
                name,
                max_velocity, 
                luck,
                predictablity,
                rotation_velocity,
                acceleration,
                start_position
                ):
        super().__init__()
        self.image = scale_image(pygame.image.load("imgs/" + name + ".png"), 0.8)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=start_position)

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
        self.name = name


    def update(self):
        self.rect.x = self.rect.x + random.randint(-10, 10)
        self.rect.y = self.rect.y + random.randint(-10, 10)
    
    def stop(self):
        self.rect.x = 200