from fastapi import HTTPException
import logging
import re
from typing import TypeVar, Optional, List
from pydantic import BaseModel, EmailStr, validator

T = TypeVar("T")

# get root logger
logger = logging.getLogger(__name__)

class ResponseView(BaseModel):
    detail: str
    result: Optional[T] = None