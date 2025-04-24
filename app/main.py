from fastapi import FastAPI,Response,HTTPException,Depends,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2

from fastapi.middleware.cors import CORSMiddleware
import time
from . import models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 


try:
    conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user='postgres',password=' ',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfull")

except Exception as error:
    print("conntion to databse failer")
    print(error)


my_posts = [{"title" : "title of post" , "content" : "content of post 1" , "id": 1 },
{"title" : "Favorite Food" , "content" : "Favorite of Food is Biriyani" , "id": 2 }]



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i





@app.get("/")
async def root():
    return {"message" : "My name is Nihal" }

@app.get("/posts")
def get_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data" : posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,db:Session=Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data" : new_post }

@app.get("/post/{id}")
def get_post(id : int,response : Response,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=404,detail=f"post with {id} was not found")
        # response.status_code = 404
        # return {"message" : f'post with {id} is not defined' }
    return {"data" : post }


@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    
    if post.first()==None:
        raise HTTPException(status_code=404,detail=f'post with {id} cannot be find')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)

@app.put("/posts/{id}")
def update_post(id : int ,updated_post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404,detail=f'post with  this id : {id} does not exists')

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data" : post_query.first()}

