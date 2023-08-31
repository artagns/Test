from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.database import get_db

from app.oauth2 import get_current_user # used for authentication

router = APIRouter(
    prefix="/likes",
    tags=["Like"]
)

@router.post("/{post_id}")
def like(post_id: int, current_user:schemas.User=Depends(get_current_user),
        db: Session=Depends(get_db)) : 

    if not db.query(models.Post).filter(models.Post.post_id==post_id).first() : # if such post doesn't exists
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This post doesn't exists!")

    like_query = db.query(models.Like).\
        filter(models.Like.post_id==post_id, models.Like.username==current_user.username)
    
    like_result = like_query.first()
    if like_result : # the user has already liked this post, so we should un-like it
        like_query.delete(synchronize_session=False)
        db.commit()
        return "un-liked"
    
    else : # the user hasn't liked this post yet, so we should like this
        like
        new_like = models.Like(**{"username": current_user.username, "post_id": post_id})
        db.add(new_like)
        db.commit()
        return "liked"



    