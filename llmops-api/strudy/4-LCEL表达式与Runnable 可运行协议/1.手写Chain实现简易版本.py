import os
from typing import Any

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1. 构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
)
parser = StrOutputParser()


class Chain:
    steps: list = []

    def __init__(self, steps: list):
        self.steps = steps

    def invoke(self, query: Any) -> Any:
        for step in self.steps:
            query = step.invoke(query)
            print("步骤:", step)
            print("结果:", query)
            print("==============================>")
        return query


chain = Chain([prompt, llm, parser])

print(chain.invoke({"query": "你好,你是?"}))
