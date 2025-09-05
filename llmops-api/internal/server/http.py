import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import json, Response, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    """http服务器引擎"""

    def __init__(self,
                 *args,
                 conf: Config,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,
                 **kwargs):
        # 调用父类构造函数初始化
        super(Http, self).__init__(*args, **kwargs)

        # 初始化应用配置
        self.config.from_object(conf)

        # 注册绑定异常处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 初始化flask 扩展 数据库
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")

        # 解决前后端跨域问题
        # CORS(self, resources={
        #     r"/*": {
        #         "origins": "*",
        #         "supports_credentials": True,
        #         # 可不配做
        #         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        #         "allow_headers": ["Content-Type", "Authorization"],
        #
        #     }
        # })

        # 注册应用路由
        router.register_router(self)

    # 处理异常
    def _register_error_handler(self, error: Exception):
        """注册异常处理"""
        # 异常信息是不是我们的自定义异常, 如果是可以提取 message 和 code 等信息
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))

        # 如果不是我们的自定义异常, 则有可能是程序\数据库的异常,也可以提取信息,设置为 FAIL 状态码
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise error

        return json(Response(
            code=HttpCode.FAIL,
            message=str(error),
            data={}
        ))
