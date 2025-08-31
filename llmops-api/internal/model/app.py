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

    id = Column(UUID, default=uuid.uuid4, nullable=False, comment="应用ID")
    account_id = Column(UUID, nullable=False, comment="应用账户ID")
    name = Column(String(255), default="", nullable=False, comment="应用名称")
    icon = Column(String(255), default="", nullable=False, comment="应用图标")
    description = Column(Text, default={}, nullable=False, comment="应用描述")
    status = Column(String(255), default="", nullable=False, comment="应用状态")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
