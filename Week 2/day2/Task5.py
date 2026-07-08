from fastapi import FastAPI
from pydantic import BaseModel,Field, field_validator

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str =Field(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
    age: int =Field(ge=18 , le=120)

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError('Name must contain only alphabetic characters')
        return value


@app.post("/users")
def user_info(user: UserCreate):
    return user