from typing import Optional

from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(..., description="The Name of the book", max_length=300)
    author: str = Field(..., description="Person who wrote the book", max_length=400)
    price: int = Field(None, description="Cost of the Book in inr", gt=10)

    class Config:
        schema_extra = {
            "example": {
                "title": "fluent python",
                "author": "luciano ramalho",
                "price": 2000
            }
        }

class UpdateBookSchema(BaseModel):
    title: Optional[str] 
    author: Optional[str]
    price: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "Fluent Python: Clear, Concise, and Effective Programming",
                "author": "Luciano Ramalho",
                "price": 2500
            }
        }


def ResponseModel(data, message):
    return{
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponse(error, code, message):
    return {"error":error, "code":code, "messge":message}