from fastapi import FastAPI, Body, Response , status , HTTPException
from pydantic import BaseModel
from typing import Optional 
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    publish: bool = True
    rating: Optional[int] = None



my_post = [{"title":"title of post 1","content":"content of post 1","id":1},
           {"title":"title of post 2","content":"content of post 2","id":2},
           {"title":"title of post 3","content":"content of post 3","id":3}]


def find_posts(id):
    for p in my_post:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message":"Welcome"}


@app.get("/posts")
async def get_post():
    return {"data":my_post}


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

@app.post("/postsbydict")
def create_post_bydict(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data":post_dict}



@app.get("/posts/latest")
def get_latest_posts():
    post = my_post[len(my_post) - 1]
    return {"details": post}


@app.get("/posts/{id}")   #post parameter
def get_post(id:int , resposnse : Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        # resposnse.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id: {id} was not found"}
    return {"post_details":post}

