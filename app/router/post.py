from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session , relationship
from typing import List

from .. import models, schemas 
from . import Oauth2
from ..databse import SessionLocal

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# 1️⃣ CREATE POST
# -------------------------
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db) , current_user :int = Depends(Oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(**post.dict(),
                           owner_id = current_user.id) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# -------------------------
# 2️⃣ READ ALL POSTS
# -------------------------
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db) , current_user :int = Depends(Oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


# -------------------------
# 3️⃣ READ SINGLE POST
# -------------------------
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user :int = Depends(Oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return post


# -------------------------
# 4️⃣ UPDATE POST
# -------------------------
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db) , current_user :int = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not Authrozed to perofrm action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# -------------------------
# 5️⃣ DELETE POST
# -------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user :int = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    if post.owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not Authrozed to perofrm action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return