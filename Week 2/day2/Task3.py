from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str =Field(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
    age: int =Field(ge=18 , le=120)
class UserRead(BaseModel):
    id: int
    name: str
    email: str =Field(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
    age: int =Field(ge=18 , le=120)

@app.post("/users", response_model=UserRead)
def user_info(user: UserCreate):
    # In a real application, you would save the user to a database here
    return {
        "id": 1,
        **user.model_dump()
    }