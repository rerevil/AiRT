import asyncio

import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras import Sequential

from constants import BATCH, CHECKPOINT_DIR, EPOCHS
from image_scraper import get_100_images_of
import os
from tensorflow.keras import layers
import time

from IPython import display

from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()

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

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='relu'))
    assert model.output_shape == (None, 300, 300, 1)

    return model


def make_discriminator_model():
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',
                            input_shape=[300, 300, 1]))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model




def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator = make_generator_model()
discriminator = make_discriminator_model()
generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def generate_and_save_images(model, epoch, test_input):
    # Notice `training` is set to False.
    # This is so all layers run in inference mode (batchnorm).
    predictions = model(test_input, training=False)

    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
        plt.axis('off')

    plt.savefig(os.path.join(CHECKPOINT_DIR, 'image_at_epoch_{:04d}.png'.format(epoch)))
    # plt.show()
    plt.close(fig)


async def checkpoint_model():
    checkpoint_prefix = os.path.join(CHECKPOINT_DIR, "ckpt")
    checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                     discriminator_optimizer=discriminator_optimizer)
    return checkpoint, checkpoint_prefix


@tf.function
def train_step(images, noise_dim):
    noise = tf.random.normal([BATCH, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))


def train(dataset, epochs, noise_dim, checkpoint, checkpoint_prefix, seed):
    for epoch in range(epochs):
        start = time.time()

        for image_batch in dataset:
            train_step(image_batch, noise_dim)

        # Produce images for the GIF as you go
        display.clear_output(wait=True)
        generate_and_save_images(generator,
                                 epoch + 1,
                                 seed)

        # Save the model every 15 epochs
        if (epoch + 1) % 15 == 0:
            checkpoint.save(file_prefix=checkpoint_prefix)

        print('Time for epoch {} is {} sec'.format(epoch + 1, time.time() - start))

    # Generate after the final epoch
    display.clear_output(wait=True)
    generate_and_save_images(generator,
                             epochs,
                             seed)


async def main():
    train_images = await get_100_images_of('cat', as_array=True)
    # train_images = train_images.reshape(train_images.shape[0], 300, 300, 1).astype('float32')
    print(train_images.shape)
    train_images = (train_images - 127.5) / 127.5  # Normalize the images to [-1, 1]

    train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(1).batch(BATCH)

    noise_dim = 100
    num_examples_to_generate = 16

    # You will reuse this seed overtime (so it's easier)
    # to visualize progress in the animated GIF)
    seed = tf.random.normal([num_examples_to_generate, noise_dim])
    checkpoint, checkpoint_prefix = await checkpoint_model()
    train(dataset=train_dataset,
          epochs=EPOCHS,
          noise_dim=noise_dim,
          checkpoint=checkpoint,
          checkpoint_prefix=checkpoint_prefix,
          seed=seed)
    generator.save("generator_model1.h5")
    

if __name__ == '__main__':
    asyncio.run(main())
