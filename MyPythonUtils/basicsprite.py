import pygame

class BasicSprite(pygame.sprite.Sprite):
  def __init__(self, image, position):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.x = position[0]
    self.rect.y = position[1]
    self.mask = pygame.mask.from_surface(self.image)
    