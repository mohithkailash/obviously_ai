from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional
from ..database import get_db
from ..models.book import Book
from ..schemas.book import BookCreate, BookUpdate, Book as BookSchema
from ..auth import get_current_user
from ..exceptions.exception_types import (
    NotFoundError, 
    DuplicateBookError,
    BookAPIException
)

router = APIRouter()

@router.post("/", response_model=BookSchema)
async def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if db.query(Book).filter(Book.title == book.title).first():
        raise DuplicateBookError(book.title)
    
    db_book = Book(**book.dict())
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise DuplicateBookError(book.title)
    except SQLAlchemyError:
        db.rollback()
        raise BookAPIException(
            status_code=500,
            detail="Database error while creating book"
        )

@router.get("/", response_model=List[BookSchema])
async def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        books = db.query(Book).offset(skip).limit(limit).all()
        return books
    except SQLAlchemyError:
        raise BookAPIException(
            status_code=500,
            detail="Database error while fetching books"
        )

@router.get("/{book_id}", response_model=BookSchema)
async def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise NotFoundError("Book", book_id)
        return book
    except SQLAlchemyError:
        raise BookAPIException(
            status_code=500,
            detail=f"Database error while fetching book {book_id}"
        )

@router.patch("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise NotFoundError("Book", book_id)

        # Check for title uniqueness if title is being updated
        if book_update.title and book_update.title != db_book.title:
            if db.query(Book).filter(Book.title == book_update.title).first():
                raise DuplicateBookError(book_update.title)
        
        update_data = book_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise DuplicateBookError(book_update.title)
    except SQLAlchemyError:
        db.rollback()
        raise BookAPIException(
            status_code=500,
            detail=f"Database error while updating book {book_id}"
        )

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise NotFoundError("Book", book_id)
        
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise BookAPIException(
            status_code=500,
            detail=f"Database error while deleting book {book_id}"
        )