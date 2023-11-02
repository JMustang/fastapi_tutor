from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


data = [
    {"id": 1, "title": "POST", "content": "Content of the post"},
    {"id": 2, "title": "POST", "content": "Content of the post"},
    {"id": 3, "title": "POST", "content": "Content of the post"},
    {"id": 4, "title": "POST", "content": "Content of the post"},
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"message": data}


@app.post("/posts")
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    data.append(post_dict)
    return {"data": post_dict}
