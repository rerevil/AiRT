from pydantic import BaseModel


class Registration(BaseModel):
    username: str
    email: str
    password: str