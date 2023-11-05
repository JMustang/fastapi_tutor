from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for post in data:
        if post["id"] == id:
            return post


data = [
    {"id": 1, "title": "POST", "content": "Content of the post"},
    {"id": 2, "title": "POST", "content": "Content of the post"},
    {"id": 3, "title": "POST", "content": "Content of the post"},
    {"id": 4, "title": "POST", "content": "Content of the post"},
]


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}


@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts():
    return {"message": data}


@app.get("/posts/{id}")
async def get_post(id: int, res: Response):
    post = find_post(id)

    if not post:
        # uma forma de retornar erros, usando duas libs que vem do FastAPI, (Response e status).
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}

        raise HTTPException(
            # Essa seria outra forma de retornar erros, usando a lib HTTPException.
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return {"message": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    data.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post = find_post(id)
    if post:
        data.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} does not exist",
    )
