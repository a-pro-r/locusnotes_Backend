# app/db/models.py
from sqlalchemy import Column, String, Float, TIMESTAMP, text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String)
    tags = Column(ARRAY(String))
    location_name = Column(String)
    location = Column(Geometry('POINT', srid=4326))
    address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                       server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP(timezone=True),
                       server_default=text('CURRENT_TIMESTAMP'))

class UserDB(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP(timezone=True),
                       server_default=text('CURRENT_TIMESTAMP'))
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)