# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import time
import pygame
import random
import math
from tools import color_definitions, move_ship, Line

pygame.init()

display_width = 800
display_height = 600

ship_img = pygame.image.load('rocket.png')
ship_midpoint = ((ship_img.get_rect().size[1]) / 2) 
ship_ht_offset = 20
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slip ship')
clock = pygame.time.Clock()

  
def ship(shipX,shipY):
  gameDisplay.blit(ship_img, (shipX, shipY))

def text_objects(text, font):
  textSurface = font.render(text, True, color_definitions['black'])
  return textSurface, textSurface.get_rect()

def checkIfCrashed(line, shipAtY):
    tipOfShip = 115
    # ship hit barrier
    if (line.x <= tipOfShip) & (line.x >= tipOfShip -10):
      # line start at top, hangs down
      if line.y == 0:
        if shipAtY < line.height:
          return True
        else:
          return False
      else:
        # line starts at bottom, rises up
        if shipAtY >= line.y:
          return True
        else:
          return False
    # ship hit boundary 
    elif ((shipAtY - (ship_midpoint - (ship_ht_offset * 2.5))) >= display_height ) or ((shipAtY - ship_midpoint + ship_ht_offset) <= 0):
      return True
    else:
      return False

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

# max height is 80-85% of safe zone from line prev to following line
def getMaxHeight(prevLine, slope, distanceBtwnLines, topOrBottom ):
  # if line extends from top length is height / else length is total - height
  # print('t or b: ' + str(topOrBottom) + ' prev line start: ' + str(prevLine.y))
  if ((topOrBottom == 0) & (prevLine.y != 0)) or ((topOrBottom == 1 ) & ( prevLine.y == 0)):
    if prevLine.y == 0:
      prevSafeZone = prevLine.height + 25
    else:
      prevSafeZone = prevLine.y - 25
      slope *= -1
    #  y = mx + b    --> b = y - mx
    yIntercept = (prevSafeZone - (slope * prevLine.x))

    shipAtNextLine = (slope * (prevLine.x + distanceBtwnLines)) + yIntercept
    # print('ship at next line:' + str(shipAtNextLine))
    max_height = (display_height - shipAtNextLine) * 0.8
    
    # print('slope is :' + str(slope))
    if slope > 0:
      max_height = display_height - max_height

    if shipAtNextLine > display_height or shipAtNextLine <= 0:
      max_height = 500
    if max_height > 500:
      max_height = 500

  else:
    # print('same starting point')
    max_height = 500
  return int(max_height)

def createLine(rocketSpeed, lineSpeed, lineList):
  distanceBtwnLines = 250

  startX = display_width+distanceBtwnLines

  slope = rocketSpeed / lineSpeed 

  topOrBottom = random.randint(0,1)
  # set line to start at top or bottom of screen
  max_height = None
  if lineList:
    max_height = getMaxHeight(lineList[-1], slope, distanceBtwnLines, topOrBottom)
    # print(max_height)
    startX = lineList[-1].x + distanceBtwnLines
  if not max_height:
    max_height = 500
  
  # print('max height: ' + str(max_height))
  line_height = random.randrange(100, max_height)
  
  if topOrBottom == 0:
    startY = 0
  else:
    startY = 600-line_height
  
  line = Line(gameDisplay, line_height, startX, startY, int(max_height))
  return line


def createLinesList(numberOfLines, rocketSpeed, lineSpeed):
  lineList = []
  counter = 0
  while counter < numberOfLines:
    line = createLine(rocketSpeed, lineSpeed, lineList)
    line.number = counter
    lineList.append(line)
    counter += 1
  return lineList

didCrash=False

# game loop
def game_loop():
  shipX = (display_width * 0.05)
  shipY = (display_height * 0.5)

  didCrash= False
  gameExit= False

  line_speed = 8
  rocketSpeed = 10
  lines = createLinesList(4, rocketSpeed, line_speed)

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
        shipY = move_ship(shipY, rocketSpeed)
        ship(shipX, shipY)
      if (keys[pygame.K_DOWN]) & (didCrash != True):
        shipY = move_ship(shipY, -rocketSpeed)
        ship(shipX, shipY)

      # check if user quit
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          gameExit = True

      gameDisplay.fill(color_definitions['pink'])

      for line in lines:
        line.drawline()
        # message_display(str(line.number), 50, (line.x, line.height))
      for line in lines:
        line.x -= line_speed
        didCrash = checkIfCrashed(line, shipY)
        if didCrash:
          break
        if line.x < 0:
          lines.remove(line)
          number = line.number
          line = createLine(rocketSpeed, line_speed, lines)
          line.number = number
          lines.append(line)
        
      if didCrash:
        crashed()

      # make game progressively more difficult every 300 points
      if score > prevScore + 300:
        prevScore = score
        line_speed += 2
        rocketSpeed += 2

      ship(shipX,shipY)

    # update screen --> params update particular item on screen, no params update entire screen
    pygame.display.update()
    # updates frames/second --> how quickly loop runs
    clock.tick(60)

game_loop()
pygame.quit()
quit()
