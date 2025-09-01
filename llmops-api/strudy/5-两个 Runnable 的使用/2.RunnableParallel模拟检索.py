import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str):
    """模拟一个检索器,传入查询 query,输出文本"""
    print("执行检索:", query)
    return "我叫小慕"


# 编排 Prompt
prompt = ChatPromptTemplate.from_template("""
请根据用户的提问回答问题,可以参考对应的上下文进行回复.

<context>
{context}
<context>

用户的问题是: {query}
""")

# 构建大模型
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
)

# 创建输出解析器
parser = StrOutputParser()

# 编排链
# chain = RunnableParallel(
#     context=retrieval,
#     query=RunnablePassthrough(),
# ) | prompt | llm | parser

# RunnablePassthrough.assign 必须是字典 
chain = RunnablePassthrough.assign(context=lambda x: retrieval(x["query"])) | prompt | llm | parser

# 调用链生成结果
# content = chain.invoke("你好, 我叫什么")

content = chain.invoke({"query": "你好, 我叫什么"})

print(content)
