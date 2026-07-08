from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class ItemCreate (BaseModel):
    name: str
    price: float = Field(gt=0, description="The price must be greater than zero")
    in_stock: bool = Field(default=True, description="Indicates if the item is in stock")

class ItemRead(BaseModel):
    name: str
    price: float
    in_stock: bool
    created_at: datetime

@app.post("/items", response_model=ItemRead)
def create_item(item: ItemCreate):
    return{
        "created_at": datetime.now(),
        **item.model_dump()
    }