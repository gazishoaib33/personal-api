from schemas import BookCreate, BookOut, BookUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Book
from schemas import BookCreate, BookOut
from auth import require_api_key

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.get("/", response_model=List[BookOut])
def get_all_books(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if status:
        query = query.filter(Book.status == status)
    return query.order_by(Book.id.desc()).all()


@router.get("/{book_id}", response_model=BookOut)
def get_one_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return book


@router.post("/", response_model=BookOut, status_code=201,
             dependencies=[Depends(require_api_key)])
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookOut,
            dependencies=[Depends(require_api_key)])
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204,
               dependencies=[Depends(require_api_key)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    db.delete(book)
    db.commit()