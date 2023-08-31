from sqlalchemy import VARCHAR, Column, TEXT, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base



# DONT FORGET TO INHERIT FROM 'Base' 
class User(Base):
    __tablename__ = "users"
    username = Column(VARCHAR(50), primary_key=True,)
    email = Column(VARCHAR(50), nullable=False)
    password = Column(TEXT, nullable=False)
    dummy_column = Column(TEXT, nullable=True)

    posts = relationship("Post", back_populates="owner")

class Post(Base) :
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    title= Column(VARCHAR(50), nullable=True)
    content = Column(TEXT, nullable=True)
    publish_date = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    owner_username = Column(VARCHAR(50), ForeignKey("users.username", ondelete="cascade"), nullable=False)

    owner = relationship("User", back_populates="posts")


class Like(Base) :
    __tablename__ = "likes"
    username = Column(VARCHAR(50), ForeignKey("users.username", ondelete="cascade"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="cascade"), primary_key=True)


class DummyTable2(Base):
    __tablename__ = "DummyTable2"
    username = Column(VARCHAR(50), primary_key=True)
    post_id = Column(Integer, nullable=True)