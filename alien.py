import pygame

class Alien(pygame.sprite.Sprite):
  def __init__(self, type, position, width, height):
    super().__init__()
    self.type = type
    path = f"Graphics/alien{type}.png"
    self.image = pygame.image.load(path)
    self.image = pygame.transform.scale(self.image, (40, 40))
    self.rect = self.image.get_rect(topleft = position)
    self.width = width
    self.height = height
    self.alienLasersGroup = pygame.sprite.Group()

  def update(self, direction):
    self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
  def __init__(self, width, image, rotation, speed, x, y):
    super().__init__()
    self.width = width
    self.image = pygame.image.load(image)
    self.image = pygame.transform.scale(self.image, (40, 40))
    self.image = pygame.transform.rotate(self.image, rotation)
    self.rect = self.image.get_rect(topleft = (x,y)) #make a variable for the x value
    self.speed = speed
    
  def update(self):
    self.rect.x += self.speed 
    if self.rect.left > self.width or self.rect.right < 0:
      self.kill()



    
    