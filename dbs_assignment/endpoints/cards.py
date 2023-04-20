import datetime
import uuid

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from enum import Enum

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal


class CardStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"

class Card(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID = None
    magstripe: str = None
    status: CardStatus = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

@router.post("/cards", response_model=Card, status_code=status.HTTP_201_CREATED)
def create_card(card: Card):
    if card.user_id is None or card.magstripe is None or card.status is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if not db.query(models.User).filter(models.User.id == card.user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if card.id is None:
        card.id = uuid.uuid4()

    new_item = models.Card(
        id = card.id,
        user_id = card.user_id,
        magstripe = card.magstripe,
        status = card.status
    )

    db.add(new_item)
    db.commit()
    db.rollback()

    return new_item

@router.get("/cards/{card_id}", response_model=Card, status_code=status.HTTP_200_OK, description="OK")
def get_card(card_id: str):
    if not db.query(models.Card).filter(models.Card.id == card_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

    card = db.query(models.Card).filter(models.Card.id == card_id).first()

    return card

@router.patch("/cards/{card_id}", response_model=Card, status_code=status.HTTP_200_OK, description="Card updated")
def update_card(card_id:str, card: Card):
    if not db.query(models.Card).filter(models.Card.id == card_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    if card.user_id is None or card.status is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")
    if not db.query(models.User).filter(models.User.id == card.user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    card_to_update = db.query(models.Card).filter(models.Card.id == card_id).first()


    card_to_update.user_id = card.user_id
    card_to_update.status = card.status

    db.commit()

    return card_to_update

@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: str):
    if not db.query(models.Card).filter(models.Card.id == card_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

    card_to_delete = db.query(models.Card).filter(models.Card.id == card_id).first()

    db.delete(card_to_delete)
    db.commit()


