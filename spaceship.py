import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
  def __init__(self, width, height):
    super().__init__()
    self.screenWIDTH = width
    self.screenHEIGHT = height
    self.image = pygame.image.load("Graphics/fairy.png")
    self.image = pygame.transform.scale(self.image, (50, 50))
    self.imageTranslucent = pygame.image.load("Graphics/fairy.png").convert_alpha()
    self.imageTranslucent = pygame.transform.scale(self.imageTranslucent, (50,50))
    self.imageTranslucent.set_alpha(210)
    
    self.rect = self.image.get_rect(midbottom = (self.screenWIDTH/2, self.screenHEIGHT-25))
    self.speed = 8
    self.lasersGroup = pygame.sprite.Group()
    self.laserReady = True
    self.laserTime = 0
    self.laserDelay = 400
    # self.laserSound = pygame.mixer.Sound("Sounds/laser.ogg")

  def getUserInput(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
      self.rect.x += self.speed

    if keys[pygame.K_LEFT]:
      self.rect.x -= self.speed

    if keys[pygame.K_SPACE] and self.laserReady:
      self.laserReady = False
      laser = Laser(self.rect.center, 8, self.screenHEIGHT, (255, 82, 66))
      self.lasersGroup.add(laser)
      self.laserTime = pygame.time.get_ticks()
      # self.laserSound.play()

  def constraintMovement(self):
    if self.rect.right > self.screenWIDTH:
      self.rect.right = self.screenWIDTH

    if self.rect.left < 0:
      self.rect.left = 0

  def rechargeLaser(self):
    if not self.laserReady:
      currentTime = pygame.time.get_ticks() #retrieves current time in millisecs
      if currentTime - self.laserTime >= self.laserDelay: #time now - time the laser was fired 
        self.laserReady = True

  def reset(self):
    self.rect = self.image.get_rect(midbottom = (self.screenWIDTH/2, self.screenHEIGHT-25))
    self.lasersGroup.empty()

  def update(self):
    self.getUserInput()
    self.constraintMovement()
    self.lasersGroup.update()
    self.rechargeLaser()