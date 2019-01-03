# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import pygame


# color definition 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (173, 145, 160)
pygame.init()

display_width = 800
display_height = 600

sprite_img = pygame.image.load('rocket.png')
sprite_midpoint = ((sprite_img.get_rect().size[1]) / 2) 
sprite_ht_offset = 20
def sprite(x,y):
  gameDisplay.blit(sprite_img, (x, y))


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit racey')
clock = pygame.time.Clock()

def is_updown_arrow_key(event):
  if event.type == pygame.KEYDOWN:
    if (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
      return True
  else:
    return False

def move_sprite(y_position, distance_to_move, move_up=False):
  if move_up:
    return y_position - distance_to_move
  else:
    return y_position + distance_to_move
# game loop
def game_loop():

  x = (display_width * 0.05)
  y = (display_height * 0.5)
  crashed = False
  gameExit= False

  while not gameExit:
    # event handling loop
    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        gameExit = True
      if is_updown_arrow_key(event):
        # while key_up is not true call move_sprite
        if event.key == pygame.K_UP:
          y = move_sprite(y, 10, True)
          sprite(x, y)
        elif event.key == pygame.K_DOWN:
          y = move_sprite(y, 20)
          sprite(x, y)


    gameDisplay.fill(pink)  
    sprite(x,y)

    # crash if user hits
    if (y - (sprite_midpoint - (sprite_ht_offset * 2.5))) >= display_height or (y - sprite_midpoint + sprite_ht_offset) <= 0:
      crashed = True 
      
    
    # update screen --> params update particular item on screen, no params update entire screen
    pygame.display.update()
    # updates frames/second --> how quickly loop runs
    clock.tick(90)

game_loop()
pygame.quit()
quit()