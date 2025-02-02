from sqlalchemy import *
from .mixins import TimeMixin
from typing import Optional
from sqlmodel import Field

class User(TimeMixin, table=true):
    __tablename__ = 'users'

    id: Optional[int] = Field(None, primary_key=True, nullable=False)
    email: Optional[str] = Field(None, unique=True, nullable=False)
    encrypted_password: Optional[str] = Field(None, nullable=False)
