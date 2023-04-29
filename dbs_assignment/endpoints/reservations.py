import datetime
import uuid

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal


class Reservation(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID = None
    publication_id: uuid.UUID = None
    created_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

@router.post("/reservations", status_code=status.HTTP_201_CREATED, description="Reservation was created", response_model=Reservation)
def create_reservation(reservation: Reservation):
    if reservation.user_id is None or reservation.publication_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if reservation.id is None:
        reservation.id = uuid.uuid4()

    if reservation.user_id == "" or reservation.publication_id == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    user = db.query(models.User).filter(models.User.id == reservation.user_id).first()

    new_item = models.Reservation(
        id = reservation.id,
        user_id = reservation.user_id,
        user = user,
        publication_id = reservation.publication_id
    )

    db.add(new_item)
    db.commit()

    return new_item

@router.get("/reservations/{reservation_id}", status_code=status.HTTP_200_OK, description="Reservation was found", response_model=Reservation)
def get_reservation(reservation_id: str):
    if not db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    return reservation


@router.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: str):
    if not db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    reservation_to_delete = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    db.delete(reservation_to_delete)
    db.commit()
