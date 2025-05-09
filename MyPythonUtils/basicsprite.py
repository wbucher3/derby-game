import pygame

class BasicSprite(pygame.sprite.Sprite):
  def __init__(self, image, position):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect(topleft=position)