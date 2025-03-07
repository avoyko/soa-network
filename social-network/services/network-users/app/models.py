from sqlalchemy import Column, String, DateTime, Date
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    login = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())