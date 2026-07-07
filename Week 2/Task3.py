from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    items = [f"Item {i}" for i in range(1, 101)]  # Fake list of 100 items
    return items[skip: skip + limit]