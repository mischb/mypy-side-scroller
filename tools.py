
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
    
