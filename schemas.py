from pydantic import BaseModel, Field
from typing import Optional

# What we ACCEPT when someone creates a book
class BookCreate(BaseModel):
    title:  str = Field(..., example="The Pragmatic Programmer")
    author: str = Field(..., example="David Thomas")
    status: str = Field("want_to_read", example="want_to_read")
    rating: Optional[int] = Field(None, ge=1, le=5, example=4)
    notes:  Optional[str] = Field(None, example="Great book on clean code")

# What we RETURN when someone requests a book
class BookOut(BaseModel):
    id:     int
    title:  str
    author: str
    status: str
    rating: Optional[int]
    notes:  Optional[str]

    class Config:
        from_attributes = True  # lets Pydantic read SQLAlchemy objects

# What we ACCEPT when someone updates a book
# Every field is Optional — you can update just one field if you want
class BookUpdate(BaseModel):
    title:  Optional[str] = None
    author: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes:  Optional[str] = None

# ── Expense schemas ───────────────────────────────────────────

class ExpenseCreate(BaseModel):
    amount:      float = Field(..., gt=0, example=12.50)
    category:    str   = Field(..., example="food")
    description: Optional[str] = Field(None, example="Lunch at cafe")
    date:        str   = Field(..., example="2025-04-22")

class ExpenseOut(BaseModel):
    id:          int
    amount:      float
    category:    str
    description: Optional[str]
    date:        str

    class Config:
        from_attributes = True