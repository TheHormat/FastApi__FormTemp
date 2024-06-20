# models.py
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import metadata, engine

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, unique=True, index=True)
)

contacts = Table(
    "contacts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user", Integer, ForeignKey("users.id")),
    Column("title", String, index=True),
    Column("message", String),
)

metadata.create_all(engine)
