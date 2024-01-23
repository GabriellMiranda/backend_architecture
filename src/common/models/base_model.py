import os

from sqlalchemy import Boolean, Column, DateTime, Integer
from datetime import datetime


class BaseModel:
    _table_args_ = {"schema": os.environ.get("SCHEMA")}

    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=False, default=2)
    modified_by = Column(Integer, nullable=False, default=2)
    deleted_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False)
