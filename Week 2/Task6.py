from fastapi import HTTPException, FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, Artificizen"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    items = [f"Item {i}" for i in range(1, 101)]  # Fake list of 100 items
    return items[skip: skip + limit]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id > 100:
        raise HTTPException(
            status_code=404,
            detail="User not found. User ID must be 100 or less."
        )
    return {"user_id": user_id}

@app.post("/ping", status_code=201)
def ping():
    return {"status": "created"}