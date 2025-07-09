from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional

Base = declarative_base()

class UserModel(Base):
    """Modelo SQLAlchemy para la tabla de usuarios."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserCreate(BaseModel):
    """Modelo Pydantic para crear usuarios."""
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    """Modelo Pydantic para usuarios."""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
