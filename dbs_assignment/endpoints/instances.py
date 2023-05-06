import datetime
import uuid
from enum import Enum

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal

class InstanceType(str, Enum):
    physical = "physical"
    ebook = "ebook"
    audiobook = "audiobook"

class InstanceStatus(str, Enum):
    available = "available"
    reserved = "reserved"
    unavailable = "unavailable"


class Instance(BaseModel):
    id: uuid.UUID = None
    type: InstanceType = None
    publisher: str = None
    year: int = None
    status: InstanceStatus = None
    publication_id: uuid.UUID = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        orm_mode = True

router = APIRouter()

db = SessionLocal()

@router.post("/instances", status_code=status.HTTP_201_CREATED, description="Instance was created", response_model=Instance)
def create_instance(instance: Instance):
    if instance.type is None or instance.publisher is None or instance.year is None or instance.status is None or instance.publication_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")

    if instance.publisher == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if not db.query(models.Publication).filter(models.Publication.id == instance.publication_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication does not exits")


    if instance.id is None:
        instance.id = uuid.uuid4()

    new_item = models.Instance(
        id = instance.id,
        type = instance.type,
        publisher = instance.publisher,
        year = instance.year,
        # status = instance.status,
        status = "available",
        publication_id = instance.publication_id,
        created_at = instance.created_at,
        updated_at = instance.updated_at
    )

    db.add(new_item)
    db.commit()

    return new_item

@router.get("/instances/{instance_id}", status_code=status.HTTP_200_OK, description="Instance was found", response_model=Instance)
def get_instance(instance_id: str):
    if not db.query(models.Instance).filter(models.Instance.id == instance_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found")

    instance = db.query(models.Instance).filter(models.Instance.id == instance_id).first()

    return instance

@router.patch("/instances/{instance_id}", status_code=status.HTTP_200_OK, description="Instance was updated", response_model=Instance)
def update_instance(instance_id: str, instance: Instance):
    if not db.query(models.Instance).filter(models.Instance.id == instance_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found")

    instance_to_update = db.query(models.Instance).filter(models.Instance.id == instance_id).first()

    if not instance.type is None:
        instance_to_update.type = instance.type
        instance_to_update.updated_at = instance.updated_at

    if not instance.publisher is None:
        if instance.publisher == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
        instance_to_update.publisher = instance.publisher
        instance_to_update.updated_at = instance.updated_at

    if not instance.year is None:
        instance_to_update.year = instance.year
        instance_to_update.updated_at = instance.updated_at

    if not instance.status is None:
        instance_to_update.status = instance.status
        instance_to_update.updated_at = instance.updated_at

    if not instance.publication_id is None:
        if not db.query(models.Publication).filter(models.Publication.id == instance.publication_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication does not exits")
        instance_to_update.publication_id = instance.publication_id
        instance_to_update.updated_at = instance.updated_at

    db.commit()

    return instance_to_update

@router.delete("/instances/{instance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instance(instance_id: str):
    if not db.query(models.Instance).filter(models.Instance.id == instance_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found")

    instance_to_delete = db.query(models.Instance).filter(models.Instance.id == instance_id).first()

    db.delete(instance_to_delete)
    db.commit()


