from fastapi import FastAPI, Response, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas,utils
from .database import engine, get_db
from .routers import post,user
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy post data for fallback/testing
my_posts = [
    {"title": "title of post", "content": "content of post 1", "id": 1},
    {"title": "Favorite Food", "content": "Favorite of Food is Biriyani", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
# Root route
@app.get("/")
async def root():
    return {"message": "My name is Nihal"}

# Get all posts



