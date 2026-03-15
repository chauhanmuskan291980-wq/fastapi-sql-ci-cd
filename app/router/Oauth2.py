from jose import JWTError , jwt
from datetime import datetime , timedelta
from .. import schemas
from fastapi import Depends , status , HTTPException
from fastapi.security import OAuth2PasswordBearer
SECERT_KEY = "SECERT_KEY_FAST_API"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINTUES = 30

Oauth_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token (data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINTUES)

    to_encode.update({"exp" : expire})
    JWTTOKEN = jwt.encode(to_encode , SECERT_KEY , algorithm=ALGORITHM)
    return  JWTTOKEN



def verify_access_token (token:str, credentials_exeception):
    try:
     payload = jwt.decode(token , SECERT_KEY , algorithms=ALGORITHM)
     id .str = payload.get("user_id")
     if id is None:
        raise credentials_exeception
     token_data = schemas.TokenData(id= id)
    
    except JWTError:
       raise credentials_exeception


def get_current_user(token:str = Depends(Oauth_schema) ):
   credentials_exeception = HTTPException(status_code=status.HTTP_404_NOT_FOUND
                                          ,detail="Could not vaildate credtionals "
                                          , headers={"WWW-Authenticate":"Bearer"})
   
   return verify_access_token(token, credentials_exeception)