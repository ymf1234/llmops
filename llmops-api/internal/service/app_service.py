import uuid
from dataclasses import dataclass

from injector import inject

from internal.model.app import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    """应用服务器了逻辑"""
    db: SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            # 创建模型实体类
            app = App(
                name="测试应用",
                account_id=uuid.uuid4(),
                icon="",
                description="",
            )
            # 将实体类添加到 session 会话中
            self.db.session.add(app)
        return app

    def get_app(self, id: uuid.UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "私人聊天机器人"
        return app

    def delete_app(self, id: uuid.UUID):
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app
