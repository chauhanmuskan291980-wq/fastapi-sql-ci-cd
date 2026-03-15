from fastapi import APIRouter , Depends ,status, HTTPException 
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import databse , schemas , models , utils 
from . import Oauth2
from ..databse import SessionLocal
router = APIRouter(tags = ['Authentication'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm = Depends() ,db:Session  = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password , user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , details = f"Invaild Password"
        )
    


    access_token = Oauth2.create_access_token(data = {"user_id" :user.id})
    return {"access token":access_token , "token_type":"bearer"}


 
