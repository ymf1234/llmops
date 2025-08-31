import os
import uuid
from dataclasses import dataclass

from flask import request
from injector import inject
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionRequest
from internal.service.app_service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def creat_app(self):
        """调用服务创建新得 APP 记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经创建成功,id 为{app.id}")

    def get_app(self, id: uuid.UUID):
        """"""
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取,名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        """"""
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功更新,名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        """"""
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除,名字是{app.name}")

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取输入
        req = CompletionRequest()
        if not req.validate():
            return validate_error_json(req.errors)

        query = request.json.get("query")
        # 2.构建OpenAI客户端
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        # 3. 得到请求响应，然后将OpenAI的响应传递给前端
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {"role": "system", "content": "你是一个聊天机器人，请根据用户的输入回复对应的信息"},
                {"role": "user", "content": query}
            ]
        )

        return success_json({"content": response.choices[0].message.content})

    def ping(self):
        raise FailException("FailException")
        # return 'pong'
