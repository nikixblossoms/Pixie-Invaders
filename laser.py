import pygame

class Laser(pygame.sprite.Sprite):

  def __init__(self, position, speed, height, colour):
    super().__init__()
    self.image = pygame.Surface((4, 15))
    self.image.fill(colour)
    self.rect = self.image.get_rect(center=position)
    self.speed = speed
    self.screenHEIGHT = height

  def update(self):
    self.rect.y -= self.speed
    if self.rect.bottom > self.screenHEIGHT or self.rect.top < 0:
      self.kill()
