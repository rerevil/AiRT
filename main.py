import os
from random import choice

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from starlette.staticfiles import StaticFiles

from API_utils.image_requests import send_request
from db_connection import depend_db, get_db
from db_management.database import engine
from db_management.models import Base, Model, User
from constants import IMAGES_PATH, RESET_DB
from utils.image_generator import generate_image

from utils.subsciption import Subscription

app = FastAPI()
os.makedirs(IMAGES_PATH, exist_ok=True)
app.mount('/images', StaticFiles(directory=IMAGES_PATH), name='images')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> User:
    user = db.query(User).filter(User.username == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong credentials')
    return user


@app.on_event("startup")
async def startup_event():
    if RESET_DB:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        db = get_db()
        default = User(
            username='default',
            password='password',
            email='r.villanueva@itsrizzoli.it',
            subscription=Subscription.premium,
        )

        cat_model = Model(
            path='cat_d_CHtQTsugAcrQ.h5',
            word='cat'
        )

        db.add(default)
        db.add(cat_model)
        db.commit()
        db.close()


@app.get("/")
async def root():
    return "Hello"


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = form_data.password
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.post("/generate_image")
async def request_image(search: str, db=Depends(depend_db), current_user=Depends(get_current_user)):
    if not (models := db.query(Model).filter(Model.word == search).all()):
        return

    model_to_use = choice(models)
    # path = generate_image(model_to_use.path, current_user.username)
    request = await send_request(db, word=search, user=current_user, model=model_to_use)
    if request:
        return request.path
    else:
        return 'Training process'


@app.post("/test")
async def test(db=Depends(depend_db)):
    if not (model := db.query(Model).first()):
        return

    return model.requests
