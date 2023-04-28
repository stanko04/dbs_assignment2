from datetime import date, timedelta, datetime
import uuid

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal


class Rental(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID = None
    publication_instance_id: uuid.UUID = None
    duration: int = None
    start_date: date = None
    end_date: date = None
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

@router.post("/rentals", status_code=status.HTTP_201_CREATED, description="Rental was created", response_model=Rental)
def create_rental(rental: Rental):

    if rental.user_id is None or rental.publication_instance_id is None or rental.duration is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if rental.id is None:
        rental.id = uuid.uuid4()

    publication_instance_publication_id = db.query(models.Instance.publication_id).filter(models.Instance.id == rental.publication_instance_id)

    reservations = db.query(models.Reservation).filter(models.Reservation.publication_id == publication_instance_publication_id)
    result_reservations = db.execute(reservations)
    reservations_all = result_reservations.scalars().all()

    if not len(reservations_all) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    new_item = models.Rental(
        id = rental.id,
        user_id = rental.user_id,
        publication_instance_id = rental.publication_instance_id,
        duration = rental.duration,
        start_date = date.today(),
        end_date = date.today() + timedelta(days=rental.duration)
    )

    db.add(new_item)
    db.commit()

    return new_item
