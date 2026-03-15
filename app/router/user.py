from fastapi import FastAPI, Body, Response , status , HTTPException , Depends , APIRouter
from pydantic import BaseModel
from typing import Optional , List 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. import models , schemas , utils
from ..databse import engine , SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router = APIRouter()

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
 


@router.post("/users" , status_code=status.HTTP_201_CREATED ,response_model=schemas.userOut )
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


@router.get("/user" , status_code=status.HTTP_200_OK)
def get_user(db:Session = Depends(get_db)):
    findUser =  db.query(models.User).all()
    print(findUser)
    return findUser 


@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.userOut)
def get_user(id: int, db: Session = Depends(get_db)):

    findUserbyId = db.query(models.User).filter(models.User.id == id).first()

    if not findUserbyId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist"
        )

    return findUserbyId
