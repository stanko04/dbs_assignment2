from dbs_assignment.database import Base
from sqlalchemy import String, Column, UUID, DateTime, Date, Enum
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






