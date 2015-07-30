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

# Recursively find pixels in a cluster.
# The stop condition is: being on a pixel that already had all of its neighbors
# checked
def find_next(x, y):

  # Neighbors
  next_x = x + 1
  prev_x = x - 1
  next_y = y + 1
  prev_y = y - 1

  # Keep them inside the image
  if prev_x < 0:
    prev_x = 0
  elif next_x >= width:
    next_x = width - 1
  if prev_y < 0:
    prev_y = 0
  elif next_y >= height:
    next_y = height - 1

  # Stop condition
  num_checked = 0
  up_checked = (x, prev_y) in checked
  right_checked = (next_x, y) in checked
  down_checked = (x, next_y) in checked
  left_checked = (prev_x, y) in checked
  
  if up_checked and right_checked and down_checked and left_checked:
    return

  # Get the neighbors
  pixel_up = bin_image.getpixel((x, prev_y))
  pixel_right = bin_image.getpixel((next_x, y))
  pixel_down = bin_image.getpixel((x, next_y))
  pixel_left = bin_image.getpixel((prev_x, y))

  # If a pixel is white, continue searching from its position
  if pixel_up == 255 and not up_checked:
    current_cluster.append((x, prev_y))
    checked.append((x, prev_y))
    find_next(x, prev_y)
  
  if pixel_right == 255 and not right_checked:
    current_cluster.append((next_x, y))
    checked.append((next_x, y))
    find_next(next_x, y)

  if pixel_down == 255 and not down_checked:
    current_cluster.append((x, next_y))
    checked.append((x, next_y))
    find_next(x, next_y)

  if pixel_left == 255 and not left_checked:
    current_cluster.append((prev_x, y))
    checked.append((prev_x, y))
    find_next(prev_x, y)

def change_direction(direction):
  direction += 1
  if direction > 3:
    direction = 0
  return direction

# Search for clusters!
start_time = time.time()
for j in range(0, height):
  for i in range(0, width):

    current_cluster = []
    pixel = bin_image.getpixel((i, j))
    
    # Black pixel: check, skip
    if pixel == 0:
      checked.append((i, j))
      continue

    # White pixel: if not checked yet, we found a cluster
    else:
      if (i, j) not in checked:
        current_cluster.append((i, j))
        checked.append((i, j))
        find_next(i, j)
        clusters.append(current_cluster)

  print(str(round(j / height * 100, 2)) + "%")

end_time = time.time()

print("clusters found: " + str(len(clusters)))
print("pixels checked: " + str(len(checked)))
print("time: " + str(end_time - start_time))
