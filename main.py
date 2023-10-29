from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/post")
async def get_posts():
    return {"data": "This is your posts!"}


@app.post("/post")
async def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"post": f"title {payload['title']}"}
