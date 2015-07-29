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

clusters = [] # A list of lists of tuples
current_cluster = [] # Current cluster being investigated
checked = [] # A list of tuples (pixels) that have already been checked
inside_cluster = False

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
  inside_cluster = (pixel == 255) and ((x, y) not in checked)
  if inside_cluster:
    not_found_count = 0
    current_cluster.append((x, y))
    checked.append((x, y))
    find_next(x, y, direction, not_found_count)
  else:
    # if (x, y) not in checked:
    checked.append((x, y))
    direction = change_direction(direction)
    not_found_count = not_found_count + 1
    if not_found_count > 3:
      return
    find_next(x, y, direction, not_found_count)

def change_direction(direction):
  direction = direction + 1
  if direction > 3:
    direction = 0
  return direction

# Search for clusters!
for y in range(0, height):
  for x in range(0, width):

    pixel = bin_image.getpixel((x, y))
    inside_cluster = (pixel == 255) and ((x, y) not in checked)
    
    if inside_cluster:
      current_cluster.append((x, y))
      checked.append((x, y))
      find_next(x, y, 0, 0)
      print("found cluster with " + str(len(current_cluster)) + " pixels")
      clusters.append(current_cluster)
      current_cluster = []
    else:
      # if (x, y) not in checked:
      checked.append((x, y))

print("number of clusters found: " + str(len(clusters)))
print("")
print("pixels checked: " + str(len(checked)))



