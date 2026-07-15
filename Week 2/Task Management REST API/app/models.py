from sqlalchemy import Integer, String, ForeignKey, Date, Column
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship
    tasks = relationship("Task", back_populates="owner", cascade="all, delete")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String(20), default="pending")
    due_date = Column(Date, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship
    owner = relationship("User", back_populates="tasks")
