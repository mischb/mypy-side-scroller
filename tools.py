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