import datetime
import uuid

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal


class User(BaseModel):
    id: uuid.UUID = None
    name: str = None
    surname: str = None
    email: str = None
    birth_date: datetime.date = None
    personal_identificator: str = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def add_user(user: User):

    if user.id is None or user.name is None or user.surname is None or user.email is None or user.birth_date is None or user.personal_identificator is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    new_item = models.User(
        id = user.id,
        name = user.name,
        surname = user.surname,
        email = user.email,
        birth_date = user.birth_date,
        personal_identificator = user.personal_identificator,
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow()
    )

    db.add(new_item)
    # try:
    db.commit()
    # except Exception as ex:
    db.rollback()

    return new_item

@router.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, description="User found")
def get_user(user_id: str):
    if not db.query(models.User).filter(models.User.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    return user

@router.patch("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, description="User updated")
def update_user(user_id: str, user: User):
    if not db.query(models.User).filter(models.User.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.name is None or user.surname is None or user.email is None or user.birth_date is None or user.personal_identificator is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()

    user.id = user_id

    if(user_to_update.email != user.email):
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    user_to_update.id = user.id
    user_to_update.name = user.name
    user_to_update.surname = user.surname
    user_to_update.email = user.email
    user_to_update.birth_date = user.birth_date
    user_to_update.personal_identificator = user.personal_identificator
    user_to_update.updated_at = datetime.datetime.utcnow()

    db.commit()

    return user_to_update






