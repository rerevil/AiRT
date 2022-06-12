import tensorflow as tf
import os, sys

from matplotlib import pyplot as plt

from constants import MODELS_PATH

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        raise Exception('Choose a prompt, Example: python GAN.py cat')

    model_path = os.path.join(MODELS_PATH, sys.argv[1])
    if not os.path.exists(model_path):
        raise Exception("File not found")

    generator = tf.keras.models.load_model(model_path, compile=False)

    noise = tf.random.normal([1, 100])
    generated_image = generator(noise, training=False)

    plt.imshow(generated_image[0, :, :, 0], cmap='gray')
    plt.show()
