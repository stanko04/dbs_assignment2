import datetime
import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

import dbs_assignment.models as models
from dbs_assignment.database import SessionLocal


class Publication(BaseModel):
    id: uuid.UUID = None
    title: str = None
    authors: list = None
    categories: list = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()

router = APIRouter()

db = SessionLocal()


# Publications

@router.post("/publications", status_code=status.HTTP_201_CREATED, description="Publication was created")
def create_publication(publication: Publication):
    if publication.title is None or publication.authors is None or publication.categories is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required information")
    if publication.title == "" or len(publication.authors) == 0 or len(publication.categories) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


    if publication.id is None:
        publication.id = uuid.uuid4()

    authors_list = []
    categories_list = []

    for item in publication.authors:
        if not db.query(models.Author).filter(models.Author.name == item["name"],models.Author.surname == item["surname"]).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author not exists")
        author = db.query(models.Author).filter(models.Author.name == item["name"], models.Author.surname == item["surname"]).first()
        authors_list.append(author)

    for item in publication.categories:
        if not db.query(models.Category).filter(models.Category.name == item).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not exists")
        category = db.query(models.Category).filter(models.Category.name == item).first()
        categories_list.append(category)

    new_item = models.Publication(
        id=publication.id,
        title=publication.title,
        authors=authors_list,
        categories = categories_list,
    )

    db.add(new_item)
    db.commit()

    data = {"id": new_item.id, "title": new_item.title, "authors": [], "categories": [], "created_at": new_item.created_at, "updated_at": new_item.updated_at}

    for item in publication.authors:
        data["authors"].append({"name": item["name"], "surname": item["surname"]})

    for item in publication.categories:
        data["categories"].append(item)

    return data

@router.get("/publications/{publication_id}", status_code=status.HTTP_200_OK, description="Publication was found")
def get_publication(publication_id: str):
    if not db.query(models.Publication).filter(models.Publication.id == publication_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")

    publication = db.query(models.Publication).filter(models.Publication.id == publication_id).first()

    publication_id = db.query(models.Publication.id).filter(models.Publication.id == publication_id).scalar()
    publication_title = db.query(models.Publication.title).filter(models.Publication.id == publication_id).scalar()

    authors = select(models.publication_authors.c.author_id).filter(models.publication_authors.c.publication_id == publication_id)
    result_authors = db.execute(authors)
    results_authors = result_authors.scalars().all()

    categories = select(models.publication_categories.c.category_id).filter(models.publication_categories.c.publication_id == publication_id)
    result_categories = db.execute(categories)
    results_categories = result_categories.scalars().all()

    created_at = db.query(models.Publication.created_at).filter(models.Publication.id == publication_id).scalar()
    updated_at = db.query(models.Publication.updated_at).filter(models.Publication.id == publication_id).scalar()


    data = {"id": publication_id,  "title": publication_title, "authors": [], "categories": [], "created_at": created_at, "updated_at": updated_at}
    for author in results_authors:
        author_name = db.query(models.Author.name).filter(models.Author.id == author).scalar()
        author_surname = db.query(models.Author.surname).filter(models.Author.id == author).scalar()
        data["authors"].append({"name": author_name, "surname": author_surname})
    for category in results_categories:
        category_name = db.query(models.Category.name).filter(models.Category.id == category).scalar()
        data["categories"].append(category_name)

    return data








