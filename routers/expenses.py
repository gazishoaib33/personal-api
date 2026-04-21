from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Expense
from schemas import ExpenseCreate, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/", response_model=List[ExpenseOut])
def get_all_expenses(
    category: Optional[str] = None,
    month:    Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    if month:                                        # e.g. ?month=2025-04
        query = query.filter(Expense.date.like(f"{month}%"))

    return query.order_by(Expense.date.desc()).all()


@router.get("/summary")
def get_summary(month: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Expense)

    if month:
        query = query.filter(Expense.date.like(f"{month}%"))

    rows  = query.all()
    total = sum(r.amount for r in rows)

    by_category = {}
    for r in rows:
        by_category[r.category] = round(
            by_category.get(r.category, 0) + r.amount, 2
        )

    return {"total": round(total, 2), "by_category": by_category}


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_one_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")

    return expense


@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    expense = Expense(**data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")

    db.delete(expense)
    db.commit()