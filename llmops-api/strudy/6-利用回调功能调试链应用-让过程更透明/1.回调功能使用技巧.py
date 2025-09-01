import os
from typing import Any, Optional, Union
from uuid import UUID

import dotenv
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


# 自定义回调处理器
class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义 LLMOps 回调处理器"""

    def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[list[str]] = None,
            metadata: Optional[dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行了")
        print("serialized:", serialized)
        print("messages:", messages)

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        print("token生成了")
        print("token:", token)


# 编排 Prompt
prompt = ChatPromptTemplate.from_template("""{query}""")

# 构建大模型
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    model_name=os.getenv("MODEL"),
)

# 创建输出解析器
parser = StrOutputParser()

# 构建链
chain = {"query": RunnablePassthrough()} | prompt | llm | parser

# 调用链并执行
# content = chain.invoke("你好,你是?", config={
#     "callbacks": [
#         StdOutCallbackHandler(), LLMOpsCallbackHandler()
#     ]
# })
#
# print(content)

content = chain.stream("你好,你是?", config={
    "callbacks": [
        StdOutCallbackHandler(), LLMOpsCallbackHandler()
    ]
})

for chunk in content:
    print(chunk, end="", flush=True)
