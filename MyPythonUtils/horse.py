import pygame
import math
import random
from MyPythonUtils.util import scale_image

def create_circle_surface(radius, color):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface


class Horse(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        # self.image = scale_image(pygame.image.load("imgs/horses/" + name + ".png"), 0.6)
        self.image = create_circle_surface(20, (0, 0, 255))
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        angle = random.randint(0, 360)
        self.speed = 8
        self.velocity = pygame.math.Vector2(self.speed, 0).rotate(angle)

    def update(self):
        self.rect.centerx += int(self.velocity.x)
        self.rect.centery += int(self.velocity.y)
        # print(self.name + " Poisiton ( x: " + str(self.rect.x) + " y: " + str(self.rect.y) + " )")

        # Bounce off screen edges
        # if self.rect.left < 0 or self.rect.right > WIDTH:
        #     self.velocity.x *= -1
        # if self.rect.top < 0 or self.rect.bottom > HEIGHT:
        #     self.velocity.y *= -1

    def bounce(self, normal):
        print("Old Velocity: " + str(self.velocity))
        self.velocity = self.velocity.reflect(normal)
        print("New Velocity: " + str(self.velocity))

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