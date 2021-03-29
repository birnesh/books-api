import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
import os

# local setting
# DATABASE_URL = config("DATABASE_URL")
DATABASE_URL = os.environ.get("DATABASE_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

database = client.books

book_collection =  database.get_collection("books_collection")

# helpers

def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "price": str(book["price"])
    }

# Retrieve all the books present in the database
async def retrieve_books():
    books = []
    async for book in book_collection.find():
        books.append(book_helper(book))
    return books

# Add a book into the database
async def add_book(book_data: dict) -> dict:
    book = await book_collection.insert_one(book_data)
    new_book = await book_collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)

# Retrieve a book by id
async def retrieve_book(id: str) -> dict:
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book:
        return book_helper(book)

# Update a book by id
async def update_book(id: str, book_data: dict) -> dict:
    if len(book_data)<1:
        return False
    book = await book_collection.find_one({"_id":ObjectId(id)})
    if book:
        updated_book = await book_collection.update_one(
            {"_id":ObjectId(id)}, {"$set":book_data}
        )
        if updated_book:
            return True
    return False

# Delete a book by id
async def delete_book(id: str):
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book:
        await book_collection.delete_one({"_id": ObjectId(id)})
        return True
