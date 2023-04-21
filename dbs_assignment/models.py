from dbs_assignment.database import Base
from sqlalchemy import String, Column, UUID, DateTime, Date, Enum, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
import uuid
import datetime
import enum


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, autoincrement=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    personal_identificator = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

class Card(Base):
    __tablename__ = 'cards'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, autoincrement=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    magstripe = Column(String(255), nullable=False)
    status = Column(Enum('active', 'inactive', 'expired', name='enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


# association_table = Table(
#     'association',
#     Base.metadata,
#     Column('customer_id', ForeignKey('customers.id')),
#     Column('product_id', ForeignKey('products.id'))
# )
#
# class Customer(Base):
#     __tablename__ = 'customers'
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(255), nullable=False)
#     products = relationship('Product', secondary=association_table, back_populates='customers')
#
#     def __repr__(self):
#         return f"<Customer {self.name}>"
#
# class Product(Base):
#     __tablename__ = 'products'
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(255), nullable=False)
#     price = Column(Integer(), nullable=False)
#     customers = relationship('Customer', secondary=association_table, back_populates='products')
#
#     def __repr__(self):
#         return f"<Product {self.name}>"

publication_authors = Table(
    'publication_authors',
    Base.metadata,
    Column('author_id', ForeignKey('authors.id')),
    Column('publication_id', ForeignKey('publications.id'))
)

publication_categories = Table(
    'publication_categories',
    Base.metadata,
    Column('category_id', ForeignKey('categories.id')),
    Column('publication_id', ForeignKey('publications.id'))
)



class Author(Base):
    __tablename__ = 'authors'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, autoincrement=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    publications = relationship('Publication', secondary=publication_authors, back_populates='authors')
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

class Category(Base):
    __tablename__ = 'categories'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, autoincrement=False)
    name = Column(String(255), nullable=False)
    publications = relationship('Publication', secondary=publication_categories, back_populates='categories')
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

class Publication(Base):
    __tablename__ = 'publications'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, autoincrement=False)
    title = Column(String(255), nullable=False)
    authors = relationship('Author', secondary=publication_authors, back_populates='publications')
    categories = relationship('Category', secondary=publication_categories, back_populates='publications')
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())









