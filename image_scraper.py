import asyncio
from io import BytesIO

import aiohttp
import numpy as np
import requests
from PIL import Image, ImageOps
from bs4 import BeautifulSoup

from constants import IMAGE_SIZE


async def get_100_images_of(search: str, as_array=False, pages=1) -> Image:
    image_links = []
    for i in range(pages):
        req = requests.get(f"https://www.freeimages.com/it/search/{search}" + (f"/{i}" if i > 1 else ""))
        html_imgs = BeautifulSoup(req.content, features='html.parser').find_all('img')
        image_links += [img['src'] for img in html_imgs if img['src'].startswith('https')]

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(get_image_from(session, image_link, as_array))
            for image_link in image_links
        ]
        images = await asyncio.gather(*tasks)
    if as_array:
        return np.concatenate([np.expand_dims(image, axis=0) for image in images], axis=0)

    return images


async def get_image_from(session, url, as_array):
    async with session.get(url) as img_req:
        content = await img_req.content.read()
        image = Image.open(BytesIO(content))
        image = ImageOps.grayscale(image)
        image = (await expand2square(image, 0)).resize(IMAGE_SIZE)
        if as_array:
            image = np.array(image)
        return image


async def expand2square(pil_img, background_color):
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
    images = await get_100_images_of('cat', as_array=True, pages=10)
    print(images.shape)
    # a = Image.fromarray(images[0].astype(np.uint8))
    # a.show()


if __name__ == '__main__':
    asyncio.run(main())
