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
        self.velocity = 10
        self.angle = random.randint(0, 360)
        self.x, self.y = start_position
        self.start_position = start_position
        self.name = name


    def update(self):
        self.velocity = 10
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        self.rect.y -= vertical
        self.rect.x -= horizontal
    
    def bounce(self):
        radians = math.radians(self.angle)
        self.rect.y += math.cos(radians) * self.velocity
        self.rect.x += math.sin(radians) * self.velocity
        self.angle = self.angle + 180 + random.randint(-50,50)
        
