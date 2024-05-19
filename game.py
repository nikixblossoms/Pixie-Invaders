import pygame
import random
from gameOverScreen import GameOverScreen
from intro import IntroScreen
from spaceship import Spaceship
from obstacle import Obstacle
from alien import Alien
from alien import MysteryShip
from laser import Laser


class Game:

  def __init__(self, width, height, screen, explosionSound):
    self.font = pygame.font.SysFont('Verdana', 60)
    self.WHITE = (255, 255, 255)
    self.screen = screen
    self.width = width
    self.height = height
    self.spaceshipGroup = pygame.sprite.GroupSingle()
    self.spaceshipGroup.add(Spaceship(width, height))
    self.obstacles = self.createObstacles()
    self.aliensGroup = pygame.sprite.Group()
    self.createAliens()
    self.aliensDirection = 1
    self.alienLasersGroup = pygame.sprite.Group()
    self.mysteryShipRightGroup = pygame.sprite.GroupSingle()
    self.mysteryShipLeftGroup = pygame.sprite.GroupSingle()
    self.lives = 3
    self.run = True
    self.score = 0
    self.highscore = 0
    self.explosionSound = explosionSound
    

  def createObstacles(self):
    obstacleWidth = 3
    gap = (self.width - (obstacleWidth)) / 5
    obstacles = []
    for i in range(4):
      offsetX = (i + 1) * gap + 1 * obstacleWidth
      obstacle = Obstacle((offsetX, self.height - 85))
      obstacles.append(obstacle)
    return obstacles

  def createAliens(self):
    for row in range(11):
      for column in range(4):
        y = column * 45 + 80
        x = row * 45

        if column == 0:
          alienType = 3
        elif column in (1,2):
          alienType = 2
        else:
          alienType = 1
    
        alien = Alien(alienType, (x, y), self.width, self.height)
        self.aliensGroup.add(alien)

  def moveAliens(self):
    self.aliensGroup.update(self.aliensDirection)

    alienSprites = self.aliensGroup.sprites()
    for alien in alienSprites:
      if alien.rect.right >= self.width:
        self.aliensDirection = -1
        self.moveAlienDown(2)
      elif alien.rect.left <= 0:
        self.aliensDirection = 1
        self.moveAlienDown(2)

  def moveAlienDown(self, distance):
    if self.aliensGroup:
      for alien in self.aliensGroup.sprites():
        alien.rect.y += distance

  def alienShootLaser(self):
    if self.aliensGroup.sprites():
      randomAlien = random.choice(self.aliensGroup.sprites())
      laserSprite = Laser(randomAlien.rect.center, -6, self.height, (59, 255, 121))
      self.alienLasersGroup.add(laserSprite)

  def createMysteryRightShip(self):
    self.mysteryShipRightGroup.add(
        MysteryShip(self.width, ("Graphics/fairyRight.png"), 360, 7, -20, 38))

  def createMysteryLeftShip(self):
    self.mysteryShipLeftGroup.add(
        MysteryShip(self.width, ("Graphics/fairyLeft.png"), 0, -7,
                    self.width - 10, 38))

  def checkCollision(self):
    #Spaceship
    
    if self.spaceshipGroup.sprite.lasersGroup:
      for laserSprite in self.spaceshipGroup.sprite.lasersGroup:
        
        aliensHit = pygame.sprite.spritecollide(laserSprite, self.aliensGroup, True)
        if aliensHit:
          self.explosionSound.play()
          for alien in aliensHit:
             self.score += alien.type * 100
             self.checkForHighscore()
             laserSprite.kill()
          
        if pygame.sprite.spritecollide(
          laserSprite, self.mysteryShipRightGroup, True):
          self.score += 500
          self.explosionSound.play()
          self.checkForHighscore()
          laserSprite.kill()
        if pygame.sprite.spritecollide(
          laserSprite, self.mysteryShipLeftGroup, True):
          self.score += 500
          self.checkForHighscore()
          laserSprite.kill()

        for obstacle in self.obstacles:
          if pygame.sprite.spritecollide(
            laserSprite, obstacle.blocksGroup, False):
            #times the obstacle is hit, attribute in obstacle class
            obstacle.timesHit += 1
            
            if obstacle.timesHit == 5:
              pygame.sprite.spritecollide(
                laserSprite, obstacle.blocksGroup, True)
            laserSprite.kill()

    #Alien Lasers
    if self.alienLasersGroup:
      for laserSprite in self.alienLasersGroup:
        if pygame.sprite.spritecollide(
          laserSprite, self.spaceshipGroup, False):
          laserSprite.kill()
          self.lives -= 1
          if self.lives == 0:
            self.gameOver()

        for obstacle in self.obstacles:
          if pygame.sprite.spritecollide(
            laserSprite, obstacle.blocksGroup, False):
            laserSprite.kill()

            obstacle.timesHit += 1

            if obstacle.timesHit == 4:
              pygame.sprite.spritecollide(
                laserSprite, obstacle.blocksGroup, True)
            laserSprite.kill()

    if self.aliensGroup:
      for alien in self.aliensGroup:
        for obstacle in self.obstacles:
          pygame.sprite.spritecollide(alien, obstacle.blocksGroup, True)

        if pygame.sprite.spritecollide(alien, self.spaceshipGroup, False):
          self.gameOver()

  def intro(self):
    intro = IntroScreen(
      self.screen, self.width, self.height, "CLICK to start", self.font, self.WHITE, self.width/5.5 + 15, self.height/2 - 30)
    intro.update()

  def gameOverScreen(self):
    gameOver = GameOverScreen(
      self.screen, self.width, self.height, "GAMEOVER!", self.font, self.WHITE, self.width/5.5 + 30, self.height/2 - 30)
    gameOver.update()
    pygame.display.update()
    
  def gameOver(self):
    self.run = False

  def reset(self):
    self.run = True
    self.lives = 3
    self.spaceshipGroup.sprite.reset()
    self.aliensGroup.empty()
    self.alienLasersGroup.empty()
    self.createAliens()
    self.mysteryShipLeftGroup.empty()
    self.mysteryShipRightGroup.empty()
    self.obstacles = self.createObstacles()
    self.score = 0

  def checkForHighscore(self):
    if self.score > self.highscore:
      self.highscore = self.score