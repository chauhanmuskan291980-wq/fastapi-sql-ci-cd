from fastapi import FastAPI, Body, Response , status , HTTPException , Depends
from pydantic import BaseModel
from typing import Optional , List 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models , schemas , utils
from .databse import engine , SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=['bcrypt'] , deprecated= 'auto')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



while True:
 try:
    conn = psycopg2.connect(host='localhost',database='posts',user='postgres',password='muskan!!!@00$',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Datbase connection was successfull!")
    break
 except Exception as error:
    print("Connecting to databse failed ")
    print("Error: ",error)
    time.sleep(2)
 

my_post = [{"title":"title of post 1","content":"content of post 1","id":1},
           {"title":"title of post 2","content":"content of post 2","id":2},
           {"title":"title of post 3","content":"content of post 3","id":3}]


def find_posts(id):
    for p in my_post:
        if p["id"] == id:
            return p
        

def find_index_post(id):
    for i ,p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message":"Welcome"}


@app.get("/posts")
async def get_post():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    print(posts)
    return {"data":posts}


@app.get("/sqlalchemy" , response_model=List[schemas.Post])
def test_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("SELECT * from post WHERE id = %s",(str(id)))
    post = cursor.fetchone()
    print(post)
    return {"Post_details": f"here is Post {post}"}


@app.post("/createposts")
async def create_post(payload:dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content {payload['content']}"}


# title str , content str 
@app.post("/createpost" , response_model = schemas.Post)
def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.post("/postsbydb", status_code=status.HTTP_201_CREATED)
def create_post_bydict(post: schemas.PostCreate):
    cursor.execute(
        "INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}



@app.get("/posts/latest")
def get_latest_posts():
    post = my_post[len(my_post) - 1]
    return {"details": post}


@app.get("/postsById/{id}")   #post parameter
def get_post(id:int , resposnse : Response , db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        # resposnse.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id: {id} was not found"}
    return {"post_details":post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db:Session = Depends(get_db)):
    # cursor.execute("DELETE FROM post WHERE id = %s returning * ",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    delete_post =  db.query(models.Post).filter(models.Post.id == id)
    deleted_post = delete_post.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exits")
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/updates/{id}")
def update_post(id: int, post: schemas.PostCreate , db:Session = Depends(get_db)):
    update_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_post.first()
    if updated_post == "None":
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist"
        )
    update_post.update(post.dict() , synchronize_session=False)
    db.commit()
    return {"data":  update_post.first()}



@app.post("/users" , status_code=status.HTTP_201_CREATED ,response_model=schemas.userOut )
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
     
     hashed_password = utils.hash(user.password)
     user.password = hashed_password
     new_user = models.User(
         **user.dict()
    )
     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return new_user


@app.get("/user" , status_code=status.HTTP_200_OK)
def get_user(db:Session = Depends(get_db)):
    findUser =  db.query(models.User).all()
    print(findUser)
    return findUser 


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.userOut)
def get_user(id: int, db: Session = Depends(get_db)):

    findUserbyId = db.query(models.User).filter(models.User.id == id).first()

    if not findUserbyId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist"
        )

    return findUserbyId

