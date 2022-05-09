import asyncio

import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras import layers, Sequential

from utils.image_scraper import get_100_images_of


def make_generator_model():
    model = Sequential()
    model.add(layers.Dense(75 * 75 * 64, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((75, 75, 64)))
    assert model.output_shape == (None, 75, 75, 64)  # Note: None is the batch size

    model.add(layers.Conv2DTranspose(32, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    assert model.output_shape == (None, 75, 75, 32)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(16, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    assert model.output_shape == (None, 150, 150, 16)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(3, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='relu'))
    assert model.output_shape == (None, 300, 300, 3)

    return model


def make_discriminator_model():
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',
                            input_shape=[28, 28, 1]))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model


cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)


def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)




async def main():
    train_images = await get_100_images_of('cat', as_array=True)
    # train_images = train_images.reshape(train_images.shape[0], 300, 300, 1).astype('float32')
    print(train_images.shape)
    train_images = (train_images - 127.5) / 127.5  # Normalize the images to [-1, 1]

    # train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(1).batch(BATCH)
    generator = make_generator_model()

    noise = tf.random.normal([1, 100])
    generated_image = generator(noise, training=False)

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    print(generated_image.shape)
    axs[0, 0].imshow(generated_image[0, :, :, 0], cmap='Reds')
    axs[0, 1].imshow(generated_image[0, :, :, 1], cmap='Greens')
    axs[1, 0].imshow(generated_image[0, :, :, 2], cmap='Blues')
    axs[1, 1].imshow(generated_image[0] * 255)
    plt.show()


if __name__ == '__main__':
    asyncio.run(main())
