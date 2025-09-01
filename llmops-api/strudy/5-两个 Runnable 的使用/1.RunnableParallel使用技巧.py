import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 编排 prompt
joke_prompt = ChatPromptTemplate.from_template(
    "请讲一个关于{subject}的冷笑话"
)

poem_prompt = ChatPromptTemplate.from_template(
    "请写一首关于{subject}的诗"
)

# 创建大模型
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
)

# 创建输出解析器
parser = StrOutputParser()

# 编排链
joke_chain = joke_prompt | llm | parser
pome_chain = poem_prompt | llm | parser

# 创建并行链
# map_chain = RunnableParallel(
#     {
#         "joke": joke_chain,
#         "poem": pome_chain 
#     }
# )

map_chain = RunnableParallel(joke=joke_chain, pome=pome_chain)

res = map_chain.invoke({"subject": "程序员"})

print(res)
