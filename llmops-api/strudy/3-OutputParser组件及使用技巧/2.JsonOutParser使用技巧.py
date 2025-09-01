import os

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

dotenv.load_dotenv()


# 创建一个 json 数据结构,用于告诉大语言模型这个 json 长什么样子
class Joke(BaseModel):
    # 冷笑话
    joke: str = Field(description="回答用户的冷笑话")

    # 冷笑话的笑点
    punchline: str = Field(description="这个冷笑话的笑点")


parser = JsonOutputParser(pydantic_object=Joke)

# print(parser.get_format_instructions())

print("=============================>")
# 构建一个提示模板
prompt = ChatPromptTemplate.from_template(
    "请根据用户的提问进行回答.\n{format_instructions}\n{query}",
).partial(format_instructions=parser.get_format_instructions())

# print(prompt.format(query="请讲一个关于程序员的冷笑话"))

# 构建一个大语言模型
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
    n=1
)

# 传递提示并解析
joke = parser.invoke(
    llm.invoke(
        prompt.invoke(
            {"query": "请讲一个关于程序员的冷笑话"}
        )
    )
)

print(joke)
