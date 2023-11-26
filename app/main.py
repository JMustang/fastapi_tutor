from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

    except Exception as erro:
        print(f"Erro: {erro}")
        time.sleep(2)

app.include_router(user.router)
app.include_router(post.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}
