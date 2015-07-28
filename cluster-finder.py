import sys
import time
from PIL import Image

if len(sys.argv) == 2:
  file_name = sys.argv[1]
else:
  print("Usage: python cluster-finder.py filename")
  sys.exit()

def get_bw_pixels(rbg_image):
  pixels = []
  width, height = rbg_image.size
  
  # Read pixels
  print("converting to bw...")
  for y in range(0, height):
    for x in range(0, width):
      bits = rbg_image.getpixel((x, y))
      sum_bits = 0
      for bit in bits:
        sum_bits = sum_bits + bit
      avg = sum_bits // 3
      pixels.append((avg))

  return pixels

# Open image
image = Image.open(file_name)
rgb_image = image.convert("RGB")

# Convert to bw
start_time = time.time()
bw_pixels = get_bw_pixels(rgb_image)
end_time = time.time()
print("time: " + str(end_time - start_time))

bw_image = Image.new("L", rgb_image.size)
bw_image.putdata(bw_pixels)
bw_image.show()
