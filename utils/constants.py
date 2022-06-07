import os

# Paths
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_PATH = os.path.join(BASE_DIR, 'images')
CHECKPOINT_DIR = os.path.join(BASE_DIR, '..', 'checkpoints')

# Images
IMAGE_SIZE = (30, 30)
SAMPLE_LEN = 100

# GAN
EPOCHS = 50
BATCH = 30


if __name__ == '__main__':
    print(BASE_DIR)