import sys
import time
import statistics
import math
from PIL import Image

# Check args
if len(sys.argv) == 2:
  file_name = sys.argv[1]
else:
  print("Usage: python find-clusters.py filename")
  sys.exit()

# Open image
image = Image.open(file_name)
bin_image = image.convert("1")
width, height = bin_image.size

clusters = [] # A list of lists of pixels (tuples)
checked = [] # A list of pixels (tuples) that have already been checked
current_cluster = []

def find_next(x, y, direction, not_found_count):

  # Update pixel position
  if direction == 0:
    y = y - 1
  elif direction == 1:
    x = x + 1
  elif direction == 2:
    y = y + 1
  else:
    x = x - 1
  
  if x < 0:
    x = 0
  elif x > width:
    x = width
  if y < 0:
    y = 0
  elif y > height:
    y = height

  # Go!
  pixel = bin_image.getpixel((x, y))

  if pixel == 0:
    checked.append((x, y))
    direction = change_direction(direction)

    # Stop condition
    not_found_count += 1
    if not_found_count > 3:
      return
    
    find_next(x, y, direction, not_found_count)

  elif (x, y) not in checked:
    current_cluster.append((x, y))
    checked.append((x, y))
    find_next(x, y, direction, 0)

def change_direction(direction):
  direction += 1
  if direction > 3:
    direction = 0
  return direction

# Search for clusters!
for j in range(0, height):
  for i in range(0, width):

    current_cluster = []
    pixel = bin_image.getpixel((i, j))
    
    if pixel == 0:
      checked.append((i, j))
      continue

    elif (i, j) not in checked:
      current_cluster.append((i, j))
      checked.append((i, j))
      find_next(i, j, 0, 0)

      if len(current_cluster) > 1:
        print("found cluster with " + str(len(current_cluster)) + " pixels")
        clusters.append(current_cluster)

print("clusters found: " + str(len(clusters)))
print("pixels checked: " + str(len(checked)))
