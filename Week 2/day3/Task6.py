from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

#  Database 

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

#  Models 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

# Create Tables
Base.metadata.create_all(bind=engine)

#  FastAPI 

app = FastAPI()

#  Dependency 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Create User 

@app.post("/users")
def create_user(
    name: str,
    email: str,
    db: Session = Depends(get_db),
):
    user = User(
        name=name,
        email=email,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

#  Create Post 

@app.post("/posts")
def create_post(
    title: str,
    content: str,
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    post = Post(
        title=title,
        content=content,
        user_id=user_id,
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

#  Get User Posts 

@app.get("/users/{user_id}/posts")
def get_user_posts(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    posts = db.query(Post).filter(Post.user_id == user_id).all()

    return posts