from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

# importing the routes
from .routers import users, login, posts, like

models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.include_router(users.router) # you can also add the prefix and tags here
app.include_router(login.router)
app.include_router(posts.router)
app.include_router(like.router)


origins = ["*"] # now it accepts every domain, you cna change it later

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root(db: Session=Depends(get_db)) :
    return "connected"

