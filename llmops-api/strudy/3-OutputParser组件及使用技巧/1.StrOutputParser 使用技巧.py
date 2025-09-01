import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 编排提示词模板
prompt = ChatPromptTemplate.from_template("{input}")

# 创建大语言模型
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
    n=1
)

# 创建字符串输出解析器
parser = StrOutputParser()
content = parser.parse("hello world")
print(content)

# 大模型生成结果并解析
print(
    parser.invoke(
        llm.invoke(
            prompt.invoke(
                {"input": "你好,你是?"}
            )
        )
    )
)
