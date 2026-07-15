from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import auth,tasks
from app.exceptions import global_exception_handler

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Task Management API",version="1.0.0")

# Global Exception Handler
app.add_exception_handler(Exception,global_exception_handler)

# CORSMiddleware 
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

# Include Routers
app.include_router(auth.router)
app.include_router(tasks.router)


# Root Route
@app.get("/")
def root():

    return {
        "message": "Task Management API is running"
    }

