from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI()

class Address(BaseModel):
    city: str
    country: str

class UserCreate(BaseModel):
    name: str
    email: str =Field(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
    age: int =Field(ge=18 , le=120)
    address: Address

@app.post("/users")
def user_info(user: UserCreate):
    return user