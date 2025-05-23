import pygame
import math
import random
from MyPythonUtils.util import scale_image

class Horse(pygame.sprite.Sprite):
    def __init__(self, name, start_position):
        super().__init__()
        self.image = scale_image(pygame.image.load("imgs/horses/" + name + ".png"), 0.65)
        # self.image = pygame.image.load("imgs/horses/" + name + ".png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=start_position)
        self.velocity = 20
        self.angle = random.randint(0, 360)
        self.start_position = start_position
        self.name = name
        self.bounce_sound = pygame.mixer.Sound('assets/bump.mp3')
        self.win_song = pygame.mixer.Sound('assets/get_ya_numbers_up.ogg')

    def update(self):
        self.velocity = 10
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        self.rect.y -= vertical
        self.rect.x -= horizontal
    
    def bounce(self):
        # move slight away from collision
        radians = math.radians(self.angle)
        self.rect.y += (math.cos(radians) * self.velocity) * 2
        self.rect.x += (math.sin(radians) * self.velocity) * 2
        pygame.mixer.Sound.play(self.bounce_sound)
        # adjust angle
        sign = random.randint(0,1)
        if sign == 0:
            self.angle = self.angle + 180 - (45 * random.randint(-1,1))

        else: 
            self.angle = self.angle - 180 + (45 * random.randint(-1,1))

    def display_celebration(self, window, center):
        pygame.mixer.Sound.play(self.win_song)
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