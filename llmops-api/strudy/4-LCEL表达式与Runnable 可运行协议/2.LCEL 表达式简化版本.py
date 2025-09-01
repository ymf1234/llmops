import os

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

# 创建链
chain = prompt | llm | parser

# 调用链得到结果
print(chain.invoke({"query": "你好, 你是?"}))
