from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Note
from schemas import NoteCreate, NoteUpdate, NoteOut
from auth import require_api_key

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=List[NoteOut])
def get_all_notes(
    tag:    Optional[str] = None,
    search: Optional[str] = None,
    db:     Session = Depends(get_db)
):
    query = db.query(Note)

    if tag:
        query = query.filter(Note.tag == tag)

    if search:
        like = f"%{search}%"
        query = query.filter(
            Note.title.ilike(like) | Note.content.ilike(like)
        )

    return query.order_by(Note.id.desc()).all()


@router.get("/{note_id}", response_model=NoteOut)
def get_one_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    return note


@router.post("/", response_model=NoteOut, status_code=201,
             dependencies=[Depends(require_api_key)])
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    note = Note(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/{note_id}", response_model=NoteOut,
            dependencies=[Depends(require_api_key)])
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=204,
               dependencies=[Depends(require_api_key)])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    db.delete(note)
    db.commit()