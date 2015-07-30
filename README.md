# cluster-finder
In today's episode: Python finds clusters of pixels in an image

### Setup

1. Install libjpeg-dev: `sudo apt-get install libjpeg-dev`

1. `pip3 install -r requirements.txt`

### How to

1. `python3 prepare-image.py filename`. That will generate several images, each being a binary version of the selected image with a different threshold level.

2. `python3 find-clusters.py outN.png`, where N is the number of the image generated in step 1.
