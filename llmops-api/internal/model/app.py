import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    UUID,
    String,
    DateTime,
    PrimaryKeyConstraint,
    Index,
    Text,
)

from internal.extension.database_extension import db


class App(db.Model):
    """AI应用基础模型"""
    __tablename__ = "app"
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        Index("app_account_id_index", "account_id"),
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)
    account_id = Column(UUID, nullable=False)
    name = Column(String(255), default="", nullable=False)
    icon = Column(String(255), default="", nullable=False)
    description = Column(Text, default={}, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
