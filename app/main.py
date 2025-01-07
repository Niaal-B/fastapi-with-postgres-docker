from fastapi import FastAPI,Response,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2

from psycopg2.extras import RealDictCursor
app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True


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
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}


@app.post("/createposts",status_code=201)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""", (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post }

@app.get("/post/{id}")
def get_post(id : int,response : Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """ ,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404,detail=f"post with {id} was not found")
        # response.status_code = 404
        # return {"message" : f'post with {id} is not defined' }
    return {"data" : post }


@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts where id = %s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=404,detail=f'post with {id} cannot be find')

    
    return Response(status_code=204)

@app.put("/posts/{id}")
def update_post(id : int ,post:Post):
    index  = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=404,detail=f'post with  this id : {id} does not exists')

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}

