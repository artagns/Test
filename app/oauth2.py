from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from . import schemas, models
from .database import get_db

from .config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def create_access_token(data: dict, expires_delta: timedelta=ACCESS_TOKEN_EXPIRE_MINUTES):
#     # the expiration time seems to have some problems here ...
#     expires_delta = timedelta(expires_delta) # for some reason, fastapi doesn't do this conversion
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + datetime.timedelta(minutes=timedelta)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 

def verify_token(token: str, credentials_exception) :
    try :
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        username = payload.get("username")
        if username :
            token_data = schemas.TokenData(username=username)
            return token_data
        else :
            raise credentials_exception
        
    except ExpiredSignatureError : # when the token is expired
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired, login again")
    except JWTError : # when the given token is wrong
        raise credentials_exception
    

def get_current_user(token:str =Depends(ouath2_scheme), db: Session=Depends(get_db)) :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect Username or Password!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_token(token , credentials_exception)
    user = db.query(models.User).filter(token.username == models.User.username).first()
    return user