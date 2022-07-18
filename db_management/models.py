from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Enum, func
from sqlalchemy.orm import relationship

from utils.subsciption import Subscription

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    daily_images = Column(Integer, default=5)
    subscription = Column(Enum(Subscription), default=Subscription.base)
    subscription_end = Column(DateTime, nullable=True)

    requests = relationship('Request', back_populates='user')


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    path = Column(String)
    word = Column(String)
    requests = relationship('Request', back_populates='model')


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    path = Column(String)
    made_in = Column(DateTime, default=func.now())
    requests = relationship('Request', back_populates='image')


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    word = Column(String)

    date_start = Column(DateTime, default=func.now())
    date_end = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)

    user = relationship('User',   uselist=False, back_populates='requests')
    model = relationship('Model', uselist=False, back_populates='requests')
    image = relationship('Image', uselist=False, back_populates='requests')
