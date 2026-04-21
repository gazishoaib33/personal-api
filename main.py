from fastapi import FastAPI
from database import engine, Base
import models
from routers import books, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Personal API")

app.include_router(books.router)
app.include_router(expenses.router)

@app.get("/")
def root():
    return {"message": "My Personal API is alive!"}