import pygame
import math
import random
from MyPythonUtils.util import scale_image

class Horse(pygame.sprite.Sprite):
    def __init__(self, name, start_position):
        super().__init__()
        self.image = scale_image(pygame.image.load("imgs/horses/" + name + ".png"), 0.8)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=start_position)
        self.velocity = 10
        self.angle = random.randint(0, 360)
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

    def display_celebration(self, window, center):
        self.image = scale_image(pygame.image.load("imgs/horses/" + self.name + ".png"), 7)
        self.rect = self.image.get_rect(center=center)
        x,y = center
        self.rect.x = x - (self.rect.width / 2)
        self.rect.y = y - (self.rect.height / 2)
        window.blit(self.image, (self.rect.x, self.rect.y))

    def display_name(self, window, center):
        white = (255, 255, 255)
        black = (0, 0, 0)
        font = pygame.font.Font('assets/Comic-Sans-MS.ttf', 120)
        text = font.render(self.name + " is Victorious!", True, white, black)
        textRect = text.get_rect()
        textRect.center = center
        window.blit(text, textRect)
        
