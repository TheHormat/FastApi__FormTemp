# schemas.py
from pydantic import BaseModel

class ContactBase(BaseModel):
    user: int
    title: str
    message: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
