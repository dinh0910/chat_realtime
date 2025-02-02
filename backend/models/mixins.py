from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import List, Optional


class TimeMixin(SQLModel):
    """Mixin for creation time and modification time"""

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class AuditMixin(SQLModel):
    """Mixin for creation time and modification time"""

    modified_by: Optional[str] = Field(None)
    company_id: Optional[str] = Field(None)
    created_by: Optional[str] = Field(None)
    is_deleted: Optional[bool] = Field(default=False)
