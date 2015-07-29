import sys
import time
import statistics
import math
from PIL import Image

# Check args
if len(sys.argv) == 2:
  file_name = sys.argv[1]
else:
  print("Usage: python prepare-image.py filename")
  sys.exit()

# Open image
image = Image.open(file_name)
rgb_image = image.convert("RGB")
width, height = rgb_image.size

# Converts an image to black and white
def get_bw_pixels(rgb_image):
  
  bw_pixels = []
  
  # Read pixels
  print("converting to bw...")
  for y in range(0, height):
    for x in range(0, width):
      bits = rgb_image.getpixel((x, y))
      sum_bits = 0
      for bit in bits:
        sum_bits = sum_bits + bit
      avg = sum_bits // 3
      bw_pixels.append(avg)

  return bw_pixels

# Binarizes the image
def binarize(bw_pixels, threshold):
  
  bin_pixels = []
  
  for p in bw_pixels:
    if p < threshold:
      bin_pixels.append(0)
    else:
      bin_pixels.append(255)
  
  return bin_pixels

# Convert to bw
start_time = time.time()
bw_pixels = get_bw_pixels(rgb_image)
end_time = time.time()
print("time: " + str(end_time - start_time))

# Get stdev of pixel values
# We use stdevs to create binarized images with different thresholds
print("calculating stdev...")
start_time = time.time()
bw_stdev = statistics.stdev(bw_pixels)
end_time = time.time()
print("time: " + str(end_time - start_time))

num_images = math.ceil(255 / bw_stdev)
for i in range(1, num_images):

  # Generate a new image, based on this stdev
  print("generating binarized images with threshold " + str(bw_stdev*i))
  start_time = time.time()
  bin_pixels = binarize(bw_pixels, bw_stdev*i)
  end_time = time.time()
  print("time: " + str(end_time - start_time))

  # Show the new image
  bw_image = Image.new("L", rgb_image.size)
  bw_image.putdata(bin_pixels)
  bw_image.save("out" + str(i) + ".png")

print("done generating " + str(num_images))
