import asyncio
from io import BytesIO

import aiohttp
import numpy as np
import requests
from PIL import Image
from bs4 import BeautifulSoup

from utils.constants import IMAGE_SIZE


async def get_100_images_of(search: str, as_array=False, normalize=False) -> Image:
    req = requests.get(f"https://www.freeimages.com/it/search/{search}")
    html_imgs = BeautifulSoup(req.content, features='html.parser').find_all('img')

    images_links = [img['src'] for img in html_imgs if img['src'].startswith('https')]
    images = []
    async with aiohttp.ClientSession() as session:
        for image_link in images_links:
            async with session.get(image_link) as img_req:
                content = await img_req.content.read()
                image = Image.open(BytesIO(content))
                image = expand2square(image, 0).resize(IMAGE_SIZE)
                if as_array:
                    image = np.array(image)/255
                    if len(image.shape) < 3:
                        new_image = np.zeros((*IMAGE_SIZE, 3))
                        new_image[:, :, 0] = image
                        new_image[:, :, 1] = image
                        new_image[:, :, 2] = image
                        # return Image.fromarray(image)
                        image = new_image
                images.append(image)
    if as_array:
        return np.concatenate([np.expand_dims(image, axis=0) for image in images], axis=0)

    return images


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


async def main():
    images = await get_100_images_of('cat', as_array=True)
    print(images.shape)
    # a = Image.fromarray(images[0].astype(np.uint8))
    # a.show()

if __name__ == '__main__':
    asyncio.run(main())
