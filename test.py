# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import time
import pygame
import random
import math

pygame.init()
display_width = 800
display_height = 600
from tools import possibleTrajectory
from gamedefs import color_definitions, move_ship, Line, getMaxHeight

ship_img = pygame.image.load('rocket.png')
bang_img = pygame.image.load('bang.png')
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
  message_display(("score: " + str(score)), 50, (display_width/2, 20))

# top / bottom
# return 0 means start at top, else start at bottom
def newLineStartingPosition(startPosition):
  if (not startPosition['top']) & (not startPosition['bottom']):
    randInt = random.randint(0,1)
    if randInt == 0:
      startPosition['top'] += 1
    else:
       startPosition['bottom'] += 1
  # as either increases, increase chances of opposite side being chosen
  if startPosition['top']:
    randInt = random.randint(0, int(startPosition['top'] * 1.5))
    # print('start position top: ' + str(startPosition['top']) + ' randInt: ' + str(randInt))
    if randInt == 0:
      startPosition['top'] += 1
      return 0
    else:
      startPosition['top'] = 0
      startPosition['bottom'] += 1
      return 1
  else:
    randInt = random.randint(0, int(startPosition['bottom']*1.5))
    # print('start position bottom: ' + str(startPosition['bottom']) + ' randInt: ' + str(randInt))
    if randInt == 0:
      startPosition['bottom'] += 1
      return 1
    else:
      startPosition['bottom'] = 0
      startPosition['top'] += 1
      return 0

  

# max height is 80-85% of safe zone from line prev to following line


def createLine(rocketSpeed, lineSpeed, lineList, startPosition):
  distanceBtwnLines = random.randint(100, 300)

  startX = display_width+distanceBtwnLines
  slope = rocketSpeed / lineSpeed 
    
  # increase the chances of opposite side 

  # todo: define algorithm to increase likelihood of new line on opposite side
  topOrBottom = newLineStartingPosition(startPosition)
  # set line to start at top or bottom of screen
  max_height = None
  if lineList:
    max_height = getMaxHeight(lineList[-1], slope, distanceBtwnLines, topOrBottom)
    # print(max_height)
    if (lineList[-1].x + distanceBtwnLines) < display_width:
      startX = display_width + 10
    else:
      startX = lineList[-1].x + distanceBtwnLines
    # startX = display_width + distanceBtwnLines
  if not max_height:
    max_height = 500
  
  # print('max height: ' + str(max_height))
  line_height = random.randrange(100, max_height)
  
  if topOrBottom == 0:
    startY = 0 # start at top
  else:
    startY = 600-line_height
  
  line = Line(gameDisplay, line_height, startX, startY, int(max_height))
  return line


def createLinesList(numberOfLines, rocketSpeed, lineSpeed, startPosition):
  lineList = []
  counter = 0
  while counter < numberOfLines:
    line = createLine(rocketSpeed, lineSpeed, lineList, startPosition)
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
  startPosition = {'top': 0, 'bottom': 0}

  lines = createLinesList(4, rocketSpeed, line_speed, startPosition)

  prevScore = 0
  score = 0
  while not gameExit:
    # if rocketSpeed != 0:
    #   slope = rocketSpeed / line_speed 
    # else: 
    #   slope = 1
    # shipTrajectoryStart, shipTrajectoryEnd = possibleTrajectory(lines[0], lines[1], slope)
    # pygame.draw.line(gameDisplay, color_definitions["black"], shipTrajectoryStart, shipTrajectoryEnd, 3)
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
          line = createLine(rocketSpeed, line_speed, lines, startPosition)
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


    # if rocketSpeed != 0:
    #   slope = rocketSpeed / line_speed 
    # else: 
    #   slope = 1
    # startLine, endLine = bestPath(lines[0], lines[1])
    # nextStart, nextEnd =  bestPath(lines[1], lines[2])

   
    # shipTrajectoryStart2, shipTrajectoryEnd2 = possibleTrajectory(lines[1], lines[2], slope)
    # pygame.draw.line(gameDisplay, color_definitions["red"], startLine, endLine, 3)
    # pygame.draw.line(gameDisplay, color_definitions["red"], nextStart, nextEnd, 3)
    # pygame.draw.line(gameDisplay, color_definitions["black"], shipTrajectoryStart2, shipTrajectoryEnd2, 3)
    # pygame.draw.line(gameDisplay, color_definitions["black"], (5,0), (5,display_height), 5)
    # pygame.draw.line(gameDisplay, color_definitions["black"], (0,display_height-5), (display_width,display_height-5), 5)

    # counter = 0
    # while counter < display_height:
    #   message_display(str(counter), 20, (25, counter))
    #   counter += 50
    # counter = 0
    # while counter < display_height:
    #   message_display(str(counter), 20, (25, counter))
    #   counter += 50
    
    # counter = 0
    # while counter < display_width:
    #   message_display(str(counter), 20, (counter, display_height - 20))
    #   counter += 50
    
    # pygame.draw.line(gameDisplay, color_definitions["red"], nextStart, nextEnd, 3)
    # event handling loop