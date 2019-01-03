# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import time
import pygame
import random
from tools import color_definitions, move_ship, Line

pygame.init()

display_width = 800
display_height = 600

ship_img = pygame.image.load('rocket.png')
ship_midpoint = ((ship_img.get_rect().size[1]) / 2) 
ship_ht_offset = 20
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit racey')
clock = pygame.time.Clock()
print(ship_img.get_rect().size)
def lines(linex, liney, linew, lineh, color):
  pygame.draw.rect(gameDisplay, color, [linex, liney, linew, lineh])

def createRandomLine():
  line_startx = display_width + 50
  topOrBottom = random.randint(0,1)
  # set line to start at top or bottom of screen
  if topOrBottom == 0:
    line_starty = 0
  else:
    line_starty = display_height-100
  line_width = random.randrange(100, 500)
  line_height = 10
  lines(line_startx, line_starty, line_width, line_height, color_definitions['black'])

  
def ship(shipX,shipY):
  gameDisplay.blit(ship_img, (shipX, shipY))

def text_objects(text, font):
  textSurface = font.render(text, True, color_definitions['black'])
  return textSurface, textSurface.get_rect()

def message_display(text, fontSize, position=None):
  displayText = pygame.font.SysFont("Abadi MT Condensed Extra Bold Regular", fontSize)
  TextSurf, TextRect = text_objects(text, displayText)
  if position:
    TextRect.center = position
  else:
    TextRect.center = ((display_width/2),(display_height/2))
  gameDisplay.blit(TextSurf, TextRect)
  pygame.display.update()

def crashed():
  message_display('You Crashed', 115)
  # game_loop()

def scoreCounter(score):
  message_display(("score: " + str(score)), 50, (70, 20))

# game loop
def game_loop():
  shipX = (display_width * 0.05)
  shipY = (display_height * 0.5)

  gameExit= False
  didCrash= False

  line_startx = display_width + 300
  line_height = random.randrange(100, 500)
  line_width = 10
  topOrBottom = random.randint(0,1)
  # set line to start at top or bottom of screen
  if topOrBottom == 0:
    line_starty = 0
  else:
    line_starty = display_height-line_height
  line_speed = 8

  newLine = Line(gameDisplay)
  anotherNewLine = Line(gameDisplay)
  prevScore = 0
  score = 0
  while not gameExit:
    # event handling loop
    if didCrash:
      line_speed = 0
      scoreCounter(score)
    else:
      score += 1
      scoreCounter(score)

    # get pressed keys to move ship
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP]) & (didCrash != True):
      shipY = move_ship(shipY, 10, True)
      ship(shipX, shipY)
    if (keys[pygame.K_DOWN]) & (didCrash != True):
      shipY = move_ship(shipY, 10)
      ship(shipX, shipY)

    # check if user quit
    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        gameExit = True


    gameDisplay.fill(color_definitions['pink']) 

    lines(line_startx, line_starty, line_width, line_height, color_definitions['black'])
    newLine.x -= 5
    anotherNewLine.x -= 3
    anotherNewLine.drawline()
    newLine.drawline()
    # make game progressively more difficult every 300 points
    if score > prevScore + 300:
      prevScore = score
      line_speed += 2

    line_startx -= line_speed
    ship(shipX,shipY)

    # crash if user hits boundary
    if (shipY - (ship_midpoint - (ship_ht_offset * 2.5))) >= display_height or (shipY - ship_midpoint + ship_ht_offset) <= 0:
      crashed()
      didCrash=True
    
    tipOfShip = 120
    # crash if user hits line
    if line_startx <= tipOfShip:
      if line_starty == 0:
        if shipY < line_height:
          didCrash=True
          crashed()
      else:
        if shipY >= line_starty:
          didCrash=True
          crashed()


    # if line is off screen display new block
    if line_startx < 0:
      # lines(line_startx, line_starty, line_width, line_height, color_definitions['black'])
      line_startx = display_width + 100
      line_height = random.randrange(100, 500)
      line_width = 10
      topOrBottom = random.randint(0,1)
      # set line to start at top or bottom of screen
      if topOrBottom == 0:
        line_starty = 0
      else:
        line_starty = display_height-line_height



    
    # update screen --> params update particular item on screen, no params update entire screen
    pygame.display.update()
    # updates frames/second --> how quickly loop runs
    clock.tick(60)

game_loop()
pygame.quit()
quit()
