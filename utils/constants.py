import os

# Paths
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_PATH = os.path.join(BASE_DIR, '../images')
CHECKPOINT_DIR = os.path.join(BASE_DIR, '../checkpoints')
MODELS_PATH = os.path.join(BASE_DIR, '../models')

for directory in [BASE_DIR,
                  IMAGES_PATH,
                  CHECKPOINT_DIR,
                  MODELS_PATH]:
    os.makedirs(directory, exist_ok=True)

# Images
IMAGE_SIZE = (28, 28)
SAMPLE_LEN = 100

# GAN
EPOCHS = 500
BATCH = 10

if __name__ == '__main__':
    print(BASE_DIR)
