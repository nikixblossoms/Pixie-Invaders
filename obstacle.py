import pygame


class Block(pygame.sprite.Sprite):

  def __init__(self, position):
    super().__init__()
    self.image = pygame.Surface((44, 8))
    self.image.fill((242, 204, 99))
    self.rect = self.image.get_rect(center = position)


class Obstacle(pygame.sprite.Sprite):
  
  def __init__(self, position):
    self.blocksGroup = pygame.sprite.Group()
    block = Block(position)
    self.blocksGroup.add(block)
    self.timesHit = 0
