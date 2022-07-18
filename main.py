import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import uvicorn
import subprocess
from random import choice

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from starlette.staticfiles import StaticFiles
from fastapi import BackgroundTasks
from sqlalchemy import or_

from API_utils.image_requests import send_request
from API_utils.pydantic_models import Registration
from db_connection import depend_db, get_db
from db_management.database import engine
from db_management.models import Request, User, Model, Image, Base
from constants import IMAGES_PATH, RESET_DB
from utils.subsciption import Subscription

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
        allow_credentials=True,
)

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
            username='admin',
            password='admin',
            email='r.villanueva@itsrizzoli.it',
            subscription=Subscription.premium,
        )

        cat_model = Model(
            path='cat_pIKUElqx_XXiFw.h5',
            word='cat'
        )

        dog_model = Model(
            path='f500dog.h5',
            word='dog'
        )

        mountain_model = Model(
            path='mountain_K-hiyXREenRPtg.h5',
            word='mountain'
        )

        face_model = Model(
            path='10000face2.h5',
            word='face'
        )

        bird_model = Model(
            path='10000face2.h5',
            word='bird'
        )

        db.add(default)
        db.add(cat_model)
        db.add(mountain_model)
        db.add(face_model)
        db.add(dog_model)
        db.add(bird_model)
        db.commit()
        db.close()


@app.get("/")
async def root():
    return "Hello"


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    print("-----------------------------------------------------------------------------------")
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    hashed_password = form_data.password
    if not hashed_password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.post("/generate_image")
async def request_image(search: str, background_tasks: BackgroundTasks, db=Depends(depend_db), current_user=Depends(get_current_user)):

    models = db.query(Model).filter(Model.word == search).all()
    if models:
        model_to_use = choice(models)
        image_path = await send_request(db, user=current_user, model=model_to_use)
        return {"path": image_path}
    else:
            
        new_req = Request(
            word=search,
            user_id=current_user.id,
        )
        db.add(new_req)
        db.commit()
        db.refresh(new_req)

        subprocess.Popen(["python", f"utils/GAN.PY {search}"], creationflags=subprocess.DETACHED_PROCESS)
        return status.HTTP_201_CREATED


@app.post("/register")
async def register(regist_form: Registration,
                    db=Depends(depend_db)):
    if db.query(User).filter(or_(User.username == regist_form.username, User.email == regist_form.email)).all():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email or username already in use')
    
    db.add(User(
            username=regist_form.username,
            password=regist_form.password,
            email=regist_form.email,
            subscription=Subscription.premium,
        ))
    db.commit()
    return {"result": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", debug='true', workers=4)