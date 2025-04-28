from fastapi import FastAPI, Response, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas,utils
from .database import engine, get_db
from .routers import post,user,auth
from .config import settings                                                                                                                                                                                                                                



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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# Root route
@app.get("/")
async def root():
    return {"message": "My name is Nihal"}

# Get all posts



