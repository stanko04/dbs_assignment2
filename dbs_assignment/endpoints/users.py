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
    if user.id == "" or user.name == "" or user.surname == "" or user.email == "" or user.birth_date == "" or user.personal_identificator == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
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
    if user.id == "" or user.name == "" or user.surname == "" or user.email == "" or user.birth_date == "" or user.personal_identificator == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()


    if(user_to_update.email != user.email):
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    if not user.name is None:
        user_to_update.name = user.name
    if not user.surname is None:
        user_to_update.surname = user.surname
    if not user.email is None:
        user_to_update.email = user.email
    if not user.birth_date is None:
        user_to_update.birth_date = user.birth_date
    if not user.personal_identificator is None:
        user_to_update.personal_identificator = user.personal_identificator

    db.commit()

    return user_to_update

# class Product(BaseModel):
#     id: int
#     name: str
#     price: int
#
#     class Config:
#         orm_mode = True
#
# class Customer(BaseModel):
#     id: int
#     name: str
#     products: Product
#
#     class Config:
#         orm_mode = True
#
# @router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
# def create_customer(customer: Customer):
#     new_item = models.Customer(
#         id = customer.id,
#         name = customer.name
#     )
#
#     db.add(new_item)
#     db.commit()
#
#
# @router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
# def create_product(product: Product):
#     new_item = models.Product(
#         id = product.id,
#         name = product.name,
#         price = product.price
#     )
#
#     db.add(new_item)
#     db.commit()
#
# @router.get("/customers/{customer_id}", response_model=Customer)
# def get_customer(customer_id: str):
#     customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
#
#     return customer






