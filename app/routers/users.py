from fastapi import Depends, HTTPException, status, APIRouter

from sqlalchemy.orm import Session

from typing import List

from app import models
from app import schemas
from app.database import get_db
from app.utils import Password

router = APIRouter( # this parts are optional ...
    prefix="/users",
    tags=["Users"], # it should be a list 
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# getting all the user's names 
@router.get("/", response_model=List[schemas.GetUser]) # since we add prefix for our router, it is equal to /users/
def get_users(db: Session=Depends(get_db)) :
    users = db.query(models.User).all()
    return users

# add new user
@router.post("/", status_code=status.HTTP_201_CREATED) 
def add_user(user: schemas.User, db: Session=Depends(get_db)) :
    username_exists = db.query(models.User).filter(models.User.username == user.username).first()
    if username_exists :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= "useraname already exists!"
        )
    user.password = Password.get_password_hash(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()


@router.get("/{username}", response_model=schemas.GetUser) # the url equals to /users/{username}
def get_user(username: str, db: Session=Depends(get_db)) :
    user = db.query(models.User).filter(models.User.username == username).first()
    if user :
        return user
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
