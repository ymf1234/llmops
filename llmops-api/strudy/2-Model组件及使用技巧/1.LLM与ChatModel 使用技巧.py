import os
from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1. 编排 prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 helpful 的助手, 请回答用户的问题,现在的时间是{now}"),
    ("human", "{query}"),
]).partial(now=datetime.now())

# 创建大语言模型
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
    n=1
)

ai_message = llm.invoke(
    prompt.invoke(
        {
            "query": "现在是几点, 请讲个笑话"
        }
    )
)

print(ai_message.type)
print(ai_message.content)
print(ai_message.response_metadata)
