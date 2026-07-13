from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine,Base
from app import models
from app.routers import auth, users, admin


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)


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
