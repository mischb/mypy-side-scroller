import pygame
import random
def move_ship(y_position, distance_to_move, move_up=False):
  if move_up:
    return y_position - distance_to_move
  else:
    return y_position + distance_to_move

color_definitions = {
  'black' : (0,0,0),
  'white' : (255,255,255),
  'red' : (255,0,0),
  'pink' : (173, 145, 160)
}

class Line():
  def __init__ (self, gamedisplay):
    line_startx = 800 + 300
    line_height = random.randrange(100, 500)
    line_width = 10
    topOrBottom = random.randint(0,1)
    # set line to start at top or bottom of screen
    if topOrBottom == 0:
      line_starty = 0
    else:
      line_starty = 600-line_height
    self.gameDisplay = gamedisplay
    self.x = line_startx
    self.y = line_starty
    self.width = line_width
    self.height = line_height
  
  def drawline(self):
    pygame.draw.rect(self.gameDisplay, (0,0,0), [self.x , self.y, self.width, self.height])
