from datetime import datetime

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    PromptTemplate,  # 文本提示模板
    ChatPromptTemplate,  # 对话提示模板
    HumanMessagePromptTemplate,  # 人类提示模板
    SystemMessagePromptTemplate,  # 系统提示模板
    MessagesPlaceholder,  # 消息占位符
)

# PromptTemplate 文本提示模板
prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
print(prompt.format(subject="机器学习"))
prompt_value = prompt.invoke({"subject": "机器学习"})
print(prompt_value.to_string())
print(prompt_value.to_messages())

# 对话提示模版
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是个聊天机器人,请根据用户的提问进行回复,当前的时间为:{now}"),
    # 有时候可能还有其他的消息,但是不确定
    MessagesPlaceholder("chat_history"),
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话"),
]).partial(now=datetime.now)  # partial 方法,设置部分参数

print("==========\n")

chat_prompt_value = chat_prompt.invoke({
    "subject": "机器学习",
    "chat_history": [
        HumanMessage("我是 xxx"),
        AIMessage("你好我是 AI,有什么可以帮到你的么")
    ]
})
print(chat_prompt_value)
print(chat_prompt_value.to_string())
