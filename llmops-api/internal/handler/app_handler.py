import os

from flask import request
from openai import OpenAI
from internal.schema.app_schema import CompletionRequest


class AppHandler:
    """应用控制器"""

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取输入
        req = CompletionRequest()
        if not req.validate():
            return req.errors

        query = request.json.get("query")
        # 2.构建OpenAI客户端
        client = OpenAI(
            # api_key="sk-pfqyfivtwdizrcikehphtlwgzqfrwgtggcfjgwabqmofwqbq",
            base_url=os.getenv("OPENAI_API_BASE")
        )
        # 3. 得到请求响应，然后将OpenAI的响应传递给前端
        response = client.chat.completions.create(
            model="THUDM/GLM-4-9B-0414",
            messages=[
                {"role": "system", "content": "你是一个聊天机器人，请根据用户的输入回复对应的信息"},
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content

    def ping(self):
        return 'pong'
