from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import database
from models import contacts, users
from schemas import Contact, ContactCreate, User
from typing import List

app = FastAPI()

# CORS conf
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "http://172.20.10.2:5500",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/contacts_page/", response_class=HTMLResponse)
async def read_contacts_page(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


@app.post("/contacts/", response_model=Contact)
async def create_contact(contact: ContactCreate):
    query = contacts.insert().values(
        user=contact.user, title=contact.title, message=contact.message
    )
    last_record_id = await database.execute(query)
    return {**contact.dict(), "id": last_record_id}


@app.get("/contacts/", response_model=List[Contact])
async def read_contacts(skip: int = 0, limit: int = 10):
    query = contacts.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/contacts/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int):
    query = contacts.select().where(contacts.c.id == contact_id)
    contact = await database.fetch_one(query)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.post("/users/", response_model=User)
async def create_user(user: User):
    query = users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
