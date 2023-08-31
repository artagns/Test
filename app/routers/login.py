from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app import schemas
from app import models
from app.utils import Password
from app.database import get_db
from app.oauth2 import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


# @router.post("/") 
# def login(user_info: schemas.UserLogin, db: Session=Depends(get_db)) :
#     input_username = user_info.username
#     input_password = user_info.password
#     user_data = db.query(models.User).filter(models.User.username == input_username).first()

#     if user_data and Password.validate_password(input_password, user_data.password):
#         # valid credentials
#         token = create_access_token(
#             data={"username": user_data.username, "email": user_data.email},
#             expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
#             )
#         return {"access_token": token, "token_type": "bearer"}
#     else :
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Credentials"
#         )

# the other way of receiving the user request
# for this type you should use "from-data" section of postman, and not "raw"
@router.post("/") 
def login(user_info: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)) :
    input_username = user_info.username
    input_password = user_info.password
    user_data = db.query(models.User).filter(models.User.username == input_username).first()

    if user_data and Password.validate_password(input_password, user_data.password):
        # valid credentials
        token = create_access_token(
            data={"username": user_data.username, "email": user_data.email},
            )
        return {"access_token": token, "token_type": "bearer"}
    else :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )