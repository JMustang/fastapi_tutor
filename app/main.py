from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models


models.Base.metadata.create_all(bind=engine)


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
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id ${id}, was not found!",
        )
    return {"message": post}
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    # if not post:
    #     raise HTTPException(
    #         # Essa seria outra forma de retornar erros, usando a lib HTTPException.
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} was not found",
    #     )


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  ",
    #     (post.title, post.content, post.published),
    # )

    # new_post = cursor.fetchone()
    # conn.commit()


@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update = post_query.first()

    if update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
