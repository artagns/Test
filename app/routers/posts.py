from fastapi import Depends, HTTPException, status, APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import func, text, or_

from app import models
from app import schemas
from app.database import get_db

from app.oauth2 import get_current_user

from typing import Optional, List

router = APIRouter(prefix="/posts", tags=["Post"])


# get all the posts
@router.get("/") # , response_model=List[schemas.PostLike]
def get_posts(db: Session=Depends(get_db), username:Optional[str]=None, limit:Optional[str]=None) :
    if username : # if the "username" query parameter is defined
        post_query = (
        db.query(models.Post, func.count(models.Like.post_id))
        .outerjoin(models.Like, models.Like.post_id==models.Post.post_id)
        .filter(models.Post.owner_username == username)
        .group_by(models.Like.post_id, models.Post.post_id)
    )
        # posts = db.query(models.Post).filter(models.Post.owner_username == username).limit(limit).all()
    else :
        post_query = (
        db.query(models.Post, func.count(models.Like.post_id))
        .outerjoin(models.Like, models.Like.post_id==models.Post.post_id)
        .group_by(models.Like.post_id, models.Post.post_id)
    )
    print(post_query)

    results = post_query.all()
    post_like = list(
        map(
            lambda pl: schemas.PostLike(post=schemas.Post.model_validate(pl[0]),
            likes=pl[1]), results
        )
    )

    return post_like
    

    ### using the given query from sqlalchemy, it doesn't fully work now and needs some fixings
    # query = text(
    # """
    # SELECT posts.* , count(likes.post_id) AS `likes`
    # FROM posts
    # INNER JOIN likes
    #     ON likes.post_id = posts.post_id
    # GROUP BY likes.post_id;
    # """)
    # result = db.execute(query)
    # output = result.fetchall()
    # return results


# get specific post
@router.get("/{post_id}")
def get_post(post_id: int, db: Session=Depends(get_db)) :
    # post_query = (
    #     db.query(models.Post, func.count(models.Like.post_id))
    #     .outerjoin(models.Like, models.Like.post_id == models.Post.post_id)
    #     .filter(models.Like.post_id == post_id)
    #     .group_by(models.Like.post_id, models.Post.post_id)
    # )
    post_query = (db.query(
        models.Post,  
        func.coalesce(func.count(models.Like.post_id), 0).label("count")
        )
        .outerjoin(models.Like, models.Post.post_id == models.Like.post_id)
        .filter(models.Post.post_id == post_id)
        .group_by(models.Post.post_id, models.Like.post_id)
    )

    post, likes = post_query.first()
    post_like = schemas.PostLike(
    post=schemas.Post.model_validate(post),
    likes=likes
    )
    if post :
        return post_like
    else  :
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nothing found")

# add post
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_song(new_post: schemas.PostReceive, db: Session=Depends(get_db),
            current_user: models.User=Depends(get_current_user)) :
    if current_user is None :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated!")
    else : # user has logged in
        new_post = models.Post(**new_post.model_dump())
        new_post.owner_username = current_user.username
        db.add(new_post) 
        db.commit()
    