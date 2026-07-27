from fastapi import FastAPI
from sqlalchemy import text

import app.models  # Registers all SQLAlchemy models

from app.api import auth, events, category
from app.core.database import Base, engine

app = FastAPI()

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(category.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Event Management System API"}


@app.get("/test-db")
def test_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": str(e)}