from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.book import Book
from ..schemas.book import BookCreate, Book as BookSchema, BookUpdate
from ..auth import get_current_user
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

router = APIRouter()

@router.post("/books/", response_model=BookSchema)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/books/", response_model=List[BookSchema])
def read_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@router.get("/books/{book_id}", response_model=BookSchema)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/books/{book_id}", response_model=BookSchema)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

# Bonus: SSE endpoint for real-time updates
@router.get("/books/stream/updates")
async def stream_updates(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            # Simulate updates (in a real app, this would come from a message queue or similar)
            data = {"timestamp": str(datetime.now()), "message": "Book update received"}
            yield f"data: {json.dumps(data)}\n\n"
            
            await asyncio.sleep(5)  # Send update every 5 seconds

    return EventSourceResponse(event_generator())