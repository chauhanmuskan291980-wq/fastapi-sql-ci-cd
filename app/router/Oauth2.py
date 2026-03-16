from jose import JWTError , jwt
from datetime import datetime , timedelta
from .. import schemas , databse , models
from fastapi import Depends , status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..databse import SessionLocal
SECERT_KEY = "SECERT_KEY_FAST_API"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINTUES = 30

Oauth_schema = OAuth2PasswordBearer(tokenUrl='login')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token (data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINTUES)

    to_encode.update({"exp" : expire})
    JWTTOKEN = jwt.encode(to_encode , SECERT_KEY , algorithm=ALGORITHM)
    return  JWTTOKEN



def verify_access_token (token:str, credentials_exeception):
    try:
     payload = jwt.decode(token , SECERT_KEY , algorithms=ALGORITHM)
     id = payload.get("user_id")
     if id is None:
        raise credentials_exeception
     token_data = schemas.TokenData(id= id)
    
    except JWTError:
       raise credentials_exeception
    
    return token_data


def get_current_user(token:str = Depends(Oauth_schema) , db:Session = Depends(get_db)):
   credentials_exeception = HTTPException(status_code=status.HTTP_404_NOT_FOUND
                                          ,detail="Could not vaildate credtionals "
                                          , headers={"WWW-Authenticate":"Bearer"})
   token = verify_access_token(token , credentials_exeception)
   user = db.query(models.User).filter(models.User.id == token.id).first()
   return  user