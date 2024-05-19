import pygame

class IntroScreen():
  def __init__(self, screen, width, height, text, font, textColour, x, y):
    self.screen = screen
    self.width = width
    self.height = height
    self.text = text
    self.font = font
    self.textColour = textColour
    self.textX = x
    self.textY = y
    self.background = pygame.image.load("Graphics/intro.png")
    self.background = pygame.transform.scale(self.background, (self.width, self.height))
    

  def drawText(self):
    img = self.font.render(self.text, True, self.textColour)
    self.screen.blit(img, (self.textX, self.textY))

  def update(self):
    self.screen.blit(self.background,(0,0))
    self.drawText()
    