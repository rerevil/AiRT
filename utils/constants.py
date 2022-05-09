import os

# Paths
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_PATH = os.path.join(BASE_DIR, "..", 'images')

# Images
IMAGE_SIZE = (300, 300)
SAMPLE_LEN = 100

# GAN
EPOCHS = 2
BATCH = 10
