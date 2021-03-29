from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_books,
    add_book,
    retrieve_book,
    update_book,
    delete_book
)

from app.server.models.book import (
    BookSchema,
    UpdateBookSchema,
    ResponseModel,
    ErrorResponse

)

router = APIRouter()

@router.post("/", response_description="Book data added into the database")
async def add_book_data(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = await add_book(book)
    return ResponseModel(new_book, "Book added successfully.")

@router.get("/", response_description="Books retrieved")
async def get_books():
    books = await retrieve_books()
    if books:
        return ResponseModel(books, "Books retrieved successfully")
    return ResponseModel(books, "Empty list returned")

@router.get("/{id}", response_description="Book retrieved successfully")
async def get_book(id: str):
    book = await retrieve_book(id)
    if book:
        return ResponseModel(book, "Book retrieved successfully")
    return ErrorResponse("An error occured", 404, "Book dosen't exist")

@router.put("/{id}", response_description="Book updated successfully")
async def update_book_data(id: str, book: UpdateBookSchema = Body(...)):
    book = {k:v for k,v in book.dict().items() if v is not None}
    updated_book = await update_book(id, book)
    if updated_book:
        return ResponseModel(
            f"Book with the id {id} updated successfully",
            "book updated successfully"
        )
    return ErrorResponse(
        "An error occured",
        404,
        "There was an error updating the book data"
    )

@router.delete("/{id}", response_description="Book deleted successfully")
async def delete_book_data(id: str):
    book = await delete_book(id)
    if book:
        return ResponseModel(
            f"Book data with id {id} deleted successfully",
            "Book data deleted successfully" 
        )
    return ErrorResponse(
        "An error occured",
        404,
        f"Book data with id {id} does not exist"
    )

