from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional 

app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    publish: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message":"Welcome"}


@app.get("/posts")
async def get_post():
    return {"data":"This is your posts"}


@app.post("/createposts")
async def create_post(payload:dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content {payload['content']}"}


# title str , content str 
@app.post("/createpost")
def create_posts(new_post:Post):
    print(new_post.title)
    print(new_post.content)
    print(new_post.publish)
    print(new_post.dict())
    return {"data":f"{new_post}"}
