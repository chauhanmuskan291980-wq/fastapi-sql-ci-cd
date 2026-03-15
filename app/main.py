from fastapi import FastAPI
from . import models
from .databse import engine 
 

from .router import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

 
app.include_router(post.router)
app.include_router(user.router)
