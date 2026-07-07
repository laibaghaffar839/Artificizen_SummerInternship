from fastapi import HTTPException, FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id > 100:
        raise HTTPException(
            status_code=404,
            detail="User not found. User ID must be 100 or less."
        )
    return {"user_id": user_id}