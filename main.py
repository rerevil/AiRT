import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from constants import IMAGES_PATH

app = FastAPI()
os.makedirs(IMAGES_PATH, exist_ok=True)
app.mount('/images', StaticFiles(directory=IMAGES_PATH), name='images')


@app.get("/")
async def root(search: str):
    return f"You are searching for {search}"
