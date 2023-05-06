from datetime import date, timedelta, datetime
import uuid
from sqlalchemy import select

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal


class Rental(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID = None
    publication_id: uuid.UUID = None
    publication_instance_id: uuid.UUID = None
    duration: int = None
    start_date: date = None
    end_date: date = None
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True

class RentalResponse(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID = None
    publication_instance_id: uuid.UUID = None
    duration: int = None
    start_date: date = None
    end_date: date = None
    status: str = None
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

@router.post("/rentals", status_code=status.HTTP_201_CREATED, response_model=RentalResponse, description="Rental was created")
def create_rental(rental: Rental):

    if rental.user_id is None or rental.publication_id is None or rental.duration is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if rental.duration > 14:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Maximal duration is 14 days")


    if rental.id is None:
        rental.id = uuid.uuid4()

    publication_instances = select(models.Instance.id).filter(models.Instance.publication_id == rental.publication_id).where(models.Instance.status == "available")
    result_publication_instances = db.execute(publication_instances)
    available_publication_instances = result_publication_instances.scalars().all()

    if len(available_publication_instances) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    get_reservations = db.query(models.Reservation.user_id).filter(models.Reservation.publication_id == rental.publication_id).order_by(models.Reservation.created_at.asc())
    result_reservations = db.execute(get_reservations)
    reservations_users = result_reservations.scalars().all()

    can_create_rental: bool = False

    if len(reservations_users) > 0:
        if len(reservations_users) >= len(available_publication_instances):
            pom = 1
            for reservation in reservations_users:
                reservation_to_delete = db.query(models.Reservation).filter(models.Reservation.publication_id == rental.publication_id,
                                                                            models.Reservation.user_id == reservation).first()
                if (reservation == rental.user_id and pom <= len(available_publication_instances) and reservation_to_delete):
                    # db.delete(reservation_to_delete)
                    # db.commit()
                    can_create_rental = True
                pom = pom + 1
        if len(reservations_users) < len(available_publication_instances):
            for reservation in reservations_users:
                reservation_to_delete = db.query(models.Reservation).filter(models.Reservation.publication_id == rental.publication_id,
                                                                            models.Reservation.user_id == reservation).first()
                # if (reservation == rental.user_id and reservation_to_delete):
                    # db.delete(reservation_to_delete)
                    # db.commit()
            can_create_rental = True
    if len(reservations_users) == 0:
        can_create_rental = True


    if can_create_rental == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    first_available_instance_id = None
    for first_instance in available_publication_instances:
        first_available_instance_id = first_instance
        break

    user = db.query(models.User).filter(models.User.id == rental.user_id).first()

    new_item = models.Rental(
        id = rental.id,
        user_id = rental.user_id,
        publication_instance_id = first_available_instance_id,
        duration = rental.duration,
        start_date = date.today(),
        end_date = date.today() + timedelta(days=rental.duration),
        status = "active",
        user = user
    )

    db.add(new_item)
    db.commit()


    return new_item

@router.get("/rentals/{rental_id}", status_code=status.HTTP_200_OK, response_model=RentalResponse, description="Rental was found")
def get_rental(rental_id: str):
    if not db.query(models.Rental).filter(models.Rental.id == rental_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental not found")

    rental = db.query(models.Rental).filter(models.Rental.id == rental_id).first()

    return rental

@router.patch("/rentals/{rental_id}", status_code=status.HTTP_200_OK, response_model=RentalResponse, description="Rental was found")
def update_rental(rental_id: str, rental:Rental):
    if not db.query(models.Rental).filter(models.Rental.id == rental_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental not found")

    if rental.duration is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    rental_to_update = db.query(models.Rental).filter(models.Rental.id == rental_id).first()

    rental_to_update.duration = rental.duration
    rental_to_update.end_date = date.today() + timedelta(days=rental.duration)

    db.commit()

    return  rental_to_update
