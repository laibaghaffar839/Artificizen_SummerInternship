from fastapi import FastAPI, Request, HTTPException # request for middleware Task2 day5
from fastapi.middleware.cors import CORSMiddleware # for CORSMiddleware Task3 day5
from fastapi.responses import JSONResponse     #for global hnadler execption task4 day5
from fastapi import BackgroundTasks           #for backgroundtasks task5 day5 
from sqlalchemy import text
from app.database import engine,Base
from app import models
from app.routers import auth, users, admin


Base.metadata.create_all(bind=engine)

app = FastAPI()


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

# middleware Task2 Day5
@app.middleware("http")
async def log_requests(request: Request, call_next):

    # before request process
    method = request.method
    path = request.url.path

    # send next route to request
    response = await call_next(request)

    # after the route execution
    status_code = response.status_code

    print(f"Method: {method} | Path: {path} | Status: {status_code}")

    return response

# global handler task4 day5
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail,
            "status": exc.status_code
        }
    )


# routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)

#end points
@app.get("/")
def home():
    return {"message": "FastAPI PostgreSQL Setup Working"}

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {
                "database": "connected",
                "result": result.scalar()
            }

    except Exception as e:
        return {
            "database": "failed",
            "error": str(e)
        }
