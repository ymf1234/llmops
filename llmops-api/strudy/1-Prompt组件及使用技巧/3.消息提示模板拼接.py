from langchain_core.prompts import ChatPromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 {helpful} 的助手"),
])

human_chat_prompt = ChatPromptTemplate.from_messages([
    ("human", "请讲一个关于{subject}的冷笑话"),
])

chat_prompt1 = system_chat_prompt + human_chat_prompt

print(chat_prompt1)

print(
    chat_prompt1.invoke({
        "helpful": "编程",
        "subject": "科学"
    })
)
