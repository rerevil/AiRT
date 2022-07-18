import secrets

import tensorflow as tf
import os
import numpy as np
from constants import MODELS_PATH, IMAGES_PATH
from PIL import Image
import tensorflow_hub as hub
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

def save_image(image, filename):
  """
    Saves unscaled Tensor Images.
    Args:
      image: 3D image tensor. [height, width, channels]
      filename: Name of the file to save.
  """
  if not isinstance(image, Image.Image):
    image = tf.clip_by_value(image, 0, 255)
    image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
  image.save(filename)
  print("Saved as %s.jpg" % filename)

def preprocess_image(image):
  """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
  """
  hr_image = tf.keras.preprocessing.image.img_to_array(image)
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)
  
def generate_image(model_name, username):
    model_path = os.path.join(MODELS_PATH, model_name)
    if not os.path.exists(model_path):
        raise Exception("File not found")

    generator = tf.keras.models.load_model(model_path, compile=False)

    noise = tf.random.normal([1, 100])
    generated_image = generator(noise, training=False)
    # print(generated_image[0, :, :, 0] * 127.5 + 127.5)
    # plt.imshow(generated_image[0, :, :, 0] * 127.5 + 127.5, cmap='gray')
    image = Image.fromarray(np.array(generated_image[0, :, :, 0] * 127.5 + 127.5)).convert('RGB')
    image = preprocess_image(image)
    SAVED_MODEL_PATH = "https://tfhub.dev/captain-pool/esrgan-tf2/1"

    esr_model = hub.load(SAVED_MODEL_PATH)
    
    fake_image = esr_model(image)
    fake_image = tf.squeeze(fake_image)

    filename = f"{username}_{model_name.split('_')[0]}_{secrets.token_urlsafe(10)}.png"
    path = os.path.join(IMAGES_PATH, filename)

    while os.path.exists(path):
        filename = f"{username}_{model_name.split('_')[0]}_{secrets.token_urlsafe(10)}.png"
        path = os.path.join(IMAGES_PATH, filename)
    save_image(tf.squeeze(fake_image), filename=path)
    return filename


if __name__ == '__main__':
 print(generate_image('sea_8fJaUWDgRbG7uw.h5', 'dude'))
