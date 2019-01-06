import pygame
import random

display_width = 800
display_height = 600

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


def getMaxHeight(prevLine, slope, distanceBtwnLines, topOrBottom ):
  if ((topOrBottom == 0) & (prevLine.y != 0)) or ((topOrBottom == 1 ) & ( prevLine.y == 0)):
    if prevLine.y == 0:
      prevSafeZone = prevLine.height + 100
      slope *= -1
    else:
      prevSafeZone = prevLine.y - 100
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
    max_height = 500
  return int(max_height)
