import pygame
import random


def move_ship(y_position, distance_to_move):
  return y_position - distance_to_move

color_definitions = {
  'black' : (0,0,0),
  'white' : (255,255,255),
  'red' : (255,0,0),
  'pink' : (173, 145, 160)
}

class Line():
  def __init__ (self, gamedisplay, line_height, line_startx, line_starty, max_height=500):
    line_width = 10
    self.gameDisplay = gamedisplay
    self.x = line_startx
    self.y = line_starty
    self.width = line_width
    self.height = line_height
  
  def drawline(self):
    drawLine = pygame.draw.rect(self.gameDisplay, (0,0,0), [self.x , self.y, self.width, self.height])
    return drawLine

# for testing --> outputs possible trajectory based on line distance and speed of ship
def possibleTrajectory(PL, NL, slope, distanceBtwnLines=250):
  offset = 50
  if PL.y == 0:
    prevSafeZone = PL.height + offset
  else:
    prevSafeZone = PL.y - offset
  slope *= -1
  if (PL.y != 0) & (NL.y != 0):
    if (PL.height > NL.height):
      slope *= -1
  elif (PL.y == 0) & (NL.y == 0):
    if (PL.height < NL.height):
      slope *= -1
  elif (PL.y != 0) & (NL.y == 0):
    if (PL.height > NL.height):
      slope *= -1
  elif (PL.y == 0) & (NL.y != 0):
    if (PL.height > NL.height):
      slope *= -1

  startLine = (PL.x, prevSafeZone)

  yIntercept = (prevSafeZone - (slope * PL.x))

  endLine = (slope * (PL.x + distanceBtwnLines)) + yIntercept
  endLine = (NL.x, endLine)
  return startLine, endLine
  # print('ship at next line:' + str(shipAtNextLine))

# testing --> displays slope between lines
def bestPath(prevLine, newLine):
  offset = 50
  if prevLine.y == 0:
    prevSafeZone = prevLine.height + offset
  else:
    prevSafeZone = prevLine.y - offset
  if newLine.y == 0:
    newSafeZone = newLine.height + offset
  else:
    newSafeZone = newLine.y - offset

  startLine = (prevLine.x, prevSafeZone)
  endLine = (newLine.x, newSafeZone)
  return startLine, endLine
    