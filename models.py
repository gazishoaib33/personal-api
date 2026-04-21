from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class Book(Base):
    __tablename__ = "books"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(200), nullable=False)
    author     = Column(String(150), nullable=False)
    status     = Column(String(20), default="want_to_read")
    rating     = Column(Integer, nullable=True)
    notes      = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Expense(Base):
    __tablename__ = "expenses"

    id          = Column(Integer, primary_key=True, index=True)
    amount      = Column(Float, nullable=False)
    category    = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    date        = Column(String(10), nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())


class Note(Base):
    __tablename__ = "notes"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(200), nullable=False)
    content    = Column(Text, nullable=False)
    tag        = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())