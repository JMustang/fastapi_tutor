from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            database="fastapi",
            cursor_factory=RealDictCursor,
        )

        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as erre:
        print(f"Erro: {erre}")
        time.sleep(2)


def find_post(id):
    for post in data:
        if post["id"] == id:
            return post


def find_post_index(id):
    for i, post in enumerate(data):
        if post["id"] == id:
            return i
    return -1


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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"message": posts}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            # Essa seria outra forma de retornar erros, usando a lib HTTPException.
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return {"message": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  ",
        (post.title, post.content, post.published),
    )

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# Falta testa
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = id
    post_index = find_post_index(id)
    data[post_index] = post_dict
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
