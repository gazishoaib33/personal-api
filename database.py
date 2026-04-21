from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# This creates a file called personal_api.db in your project folder
DATABASE_URL = "sqlite:///./personal_api.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# This function gives each route its own database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()