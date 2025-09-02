import os
import uuid
from dataclasses import dataclass

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

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

    def debug(self, app_id: uuid.UUID):
        """聊天接口"""
        # 1.提取从接口中获取输入
        req = CompletionRequest()
        if not req.validate():
            return validate_error_json(req.errors)

        # 构建提示词
        prompt = ChatPromptTemplate.from_template("{query}")

        # query = request.json.get("query")

        # 2.构建OpenAI客户端
        llm = ChatOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv("OPENAI_API_BASE"),
            model=os.getenv("MODEL")
        )
        # client = OpenAI(
        #     api_key=os.getenv('OPENAI_API_KEY'),
        #     base_url=os.getenv("OPENAI_API_BASE")
        # )
        # 3. 得到请求响应，然后将OpenAI的响应传递给前端
        # ai_message = llm.invoke(prompt.format_prompt(query=req.query.data))
        # response = client.chat.completions.create(
        #     model=os.getenv("MODEL"),
        #     messages=[
        #         {"role": "system", "content": "你是一个聊天机器人，请根据用户的输入回复对应的信息"},
        #         {"role": "user", "content": req.query.data}
        #     ]
        # )
        # 构建解析器
        parser = StrOutputParser()

        # content = parser.invoke(ai_message)

        # 构建链
        chain = prompt | llm | parser
        content = chain.invoke(
            {
                "query": req.query.data
            }
        )

        # return success_json({"content": response.choices[0].message.content})
        return success_json({"content": content})

    def ping(self):
        raise FailException("FailException")
        # return 'pong'
