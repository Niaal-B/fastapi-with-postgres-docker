from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None



my_posts = [{"title" : "title of post" , "content" : "content of post 1" , "id": 1 },
{"title" : "Favorite Food" , "content" : "Favorite of Food is Biriyani" , "id": 2 }]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 

@app.get("/")
async def root():
    return {"message" : "My name is Nihal" }

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


@app.post("/createposts")
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data" : post_dict }

@app.get("/post/{id}")
def get_post(id : int):
    post = find_post(id)
    return {"data" : post }