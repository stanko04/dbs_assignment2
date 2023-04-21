import datetime
import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal

class Author(BaseModel):
    id: uuid.UUID = None
    name: str = None
    surname: str = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

# Authors

@router.post("/authors", response_model=Author, status_code=status.HTTP_201_CREATED, description="Author was crated")
def create_author(author: Author):
    if author.name is None or author.surname is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if author.name == "" or author.surname == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if db.query(models.Author).filter(models.Author.name == author.name, models.Author.surname == author.surname).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author with this name and surname already exits")

    if author.id is None:
        author.id = uuid.uuid4()

    new_item = models.Author(
        id = author.id,
        name = author.name,
        surname = author.surname
    )

    db.add(new_item)
    db.commit()

    return new_item

@router.get("/authors/{author_id}", response_model=Author, status_code=status.HTTP_200_OK, description="Author was found")
def get_author(author_id: str):
    if not db.query(models.Author).filter(models.Author.id == author_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    return author

@router.patch("/authors/{author_id}", response_model=Author, status_code=status.HTTP_200_OK, description="Author informations was updated")
def update_author(author_id: str, author: Author):
    if not db.query(models.Author).filter(models.Author.id == author_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    if author.name is None and author.surname is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if author.name == "" or author.surname == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    author_to_update = db.query(models.Author).filter(models.Author.id == author_id).first()

    if db.query(models.Author).filter(models.Author.name == author.name, models.Author.surname == author.surname).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author with this name and surname already exits")

    if not author.name is None:
        author_to_update.name = author.name
    if not author.surname is None:
        author_to_update.surname = author.surname


    db.commit()

    return author_to_update

@router.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: str):
    if not db.query(models.Author).filter(models.Author.id == author_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    author_to_delete = db.query(models.Author).filter(models.Author.id == author_id).first()

    db.delete(author_to_delete)
    db.commit()
