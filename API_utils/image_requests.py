import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from db_connection import get_db
from db_management.models import Request, User, Model, Image
from utils.image_generator import generate_image


async def send_request(db: Session, *, word: str, user: User, model: Optional[Model]) -> Optional[Image]:
    if model:
        new_image = await create_image(db, model, user)

        new_req = Request(
            word=model.word,
            user_id=user.id,
            model_id=model.id,
            image_id=new_image.id,
            date_end=datetime.now()
        )
        db.add(new_req)
        db.commit()
        return new_image

    else:
        new_req = Request(
            word=word,
            user_id=user.id,
        )
        db.add(new_req)
        db.commit()
        db.refresh(new_req)

        asyncio.ensure_future(training_gen(word, user.username, new_req.id))


async def training_gen(word, user_id, request_id):
    from utils.GAN import train_generator
    new_path_model = await train_generator(word)
    new_model = Model(
        path=new_path_model,
        word=word
    )
    db = get_db()
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    user = db.query(User).filter(User.id == user_id).first()

    new_image = await create_image(db, new_model, user)

    request = db.query(Request).filter(Request.id == request_id).first()
    request.date_end = datetime.now()
    request.model_id = new_model.id
    request.image_id = new_image.id

    db.add(request)
    db.commit()
    db.close()


async def create_image(db, model, user):
    path = generate_image(model.path, user.username)
    new_image = Image(path=path)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image
