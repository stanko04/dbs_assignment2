import datetime
import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal



class Category(BaseModel):
    id: uuid.UUID = None
    name: str = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        orm_mode = True


router = APIRouter()

db = SessionLocal()

# Categories

@router.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED, description="Category was created")
def create_category(category: Category):
    if category.name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if category.name == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if db.query(models.Category).filter(models.Category.name == category.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This category already exits")

    if category.name.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if category.id is None:
        category.id = uuid.uuid4()

    new_item = models.Category(
        id = category.id,
        name = category.name
    )

    db.add(new_item)
    db.commit()

    return new_item

@router.get("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK, description="Category was found")
def get_category(category_id: str):
    if not db.query(models.Category).filter(models.Category.id == category_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    return category

@router.patch("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK, description="Category informations was updated")
def update_category(category_id: str, category: Category):
    if not db.query(models.Category).filter(models.Category.id == category_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if category.name is None or category.name == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if db.query(models.Category).filter(models.Category.name == category.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This category already exits")

    if category.name.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


    category_to_update = db.query(models.Category).filter(models.Category.id == category_id).first()

    category_to_update.name = category.name

    db.commit()

    return category_to_update

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    if not db.query(models.Category).filter(models.Category.id == category_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category_to_delete = db.query(models.Category).filter(models.Category.id == category_id).first()

    db.delete(category_to_delete)
    db.commit()
