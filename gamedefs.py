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
