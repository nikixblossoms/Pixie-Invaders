import pygame
import random
from game import Game

pygame.init()

HEIGHT = 400
WIDTH = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 220, 255)
transparency = 140

# FONTS
font = pygame.font.SysFont('Verdana', 20)
levelSurface = font.render("LEVEL 01", False, BLACK)
gameOverSurface = font.render("GAME OVER", False, BLACK)
scoreTextSurface = font.render("SCORE:", False, BLACK)
highscoreTextSurface = font.render("HIGHSCORE:", False, BLACK)

# IMAGES
background = pygame.image.load("Graphics/intro.png")
background = pygame.transform.scale(background,(WIDTH, HEIGHT))

# SOUNDS
pygame.mixer.init()
explosionSound = pygame.mixer.Sound('explosion.ogg')
laserSound = pygame.mixer.Sound('laser.ogg')
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)

# GAME CLASS
game = Game(WIDTH, HEIGHT, screen, explosionSound)

# MAIN
gameOn = True
clickStart = True
laserReady = True
laserTime = 0
laserDelay = 500

isNextShipRight = True
shipEnterScreenTime = 0
mysteryDelay = random.randint(10000, 15000)

def drawRectangle():
  rectangle = pygame.draw.rect(surface, (161, 221, 255, transparency), (0, 0, WIDTH, 35))
  pygame.display.update()
  return rectangle

while clickStart:
  game.intro()
  pygame.display.update()

  for event in pygame.event.get():
    # keys = pygame.key.get_pressed() .. if keys[pygame.K_SPACE]
    if event.type == pygame.MOUSEBUTTONDOWN:
        clickStart = False
        # ticks = pygame.time.get_ticks()
        # seconds = int(ticks/1000 % 60)
        # startTime = startTime+seconds


while gameOn:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameOn = False

    if event.type == pygame.MOUSEBUTTONDOWN and game.run == False:
      game.reset()
  
  # UPDATING
  if game.run:
    game.spaceshipGroup.update()
    game.moveAliens()
    game.alienLasersGroup.update()
    game.mysteryShipRightGroup.update()
    game.mysteryShipLeftGroup.update()
    game.checkCollision()

  # DRAWING
    screen.blit(background,(0,0))
    screen.blit(surface, (0,0))
    drawRectangle()
    game.spaceshipGroup.draw(screen)
    game.spaceshipGroup.sprite.lasersGroup.draw(screen)
    for obstacle in game.obstacles:
      obstacle.blocksGroup.draw(screen)
    game.aliensGroup.draw(screen)
    game.alienLasersGroup.draw(screen)
    game.mysteryShipRightGroup.draw(screen)
    game.mysteryShipLeftGroup.draw(screen)

  
  # UI
  if game.run:
    screen.blit(levelSurface, (280,7))
    x = 50
    for life in range(game.lives):
      screen.blit(game.spaceshipGroup.sprite.imageTranslucent, (x, 330))

      x += 50

    screen.blit(scoreTextSurface, (40,7))
    scoreSurface = font.render(str(game.score), False, BLACK)
    screen.blit(scoreSurface, (120, 7))
    screen.blit(highscoreTextSurface, (450,7))
    highscoreSurface = font.render(str(game.highscore), False, BLACK)
    screen.blit(highscoreSurface, (595, 7))
  else:
    # screen.blit(gameOverSurface, (50,50))
    game.gameOverScreen()
    

  #Debounce for alien lasers
  while laserReady and game.run:
    game.alienShootLaser()
    laserReady = False
    laserTime = pygame.time.get_ticks()

  if not laserReady and game.run:
    currentTime = pygame.time.get_ticks()
    if currentTime - laserTime >= laserDelay:
      laserReady = True

  #Timer for mystery ship
  if isNextShipRight and game.run:
    currentTime = pygame.time.get_ticks()
    if currentTime - shipEnterScreenTime >= mysteryDelay and not game.mysteryShipRightGroup:
      game.createMysteryRightShip()
      # isNextShipRight
      isNextShipRight = False
      # shipEnterScreenTime
      shipEnterScreenTime = pygame.time.get_ticks() 

  elif not isNextShipRight and game.run:
    currentTime = pygame.time.get_ticks()
    if currentTime - shipEnterScreenTime >= mysteryDelay and not game.mysteryShipLeftGroup:
      game.createMysteryLeftShip()
      shipEnterScreenTime = pygame.time.get_ticks()
      isNextShipRight = True

  pygame.display.update()
  clock.tick(60)
  pygame.time.delay(50)

pygame.quit()
