from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# 描述模板
instruction_prompt = PromptTemplate.from_template("你正在模拟{person}")

# 示例模板
example_prompt = PromptTemplate.from_template("""下面是一个交互例子:

Q: {example_q}
A: {example_a}
""")

# 开始模板
start_prompt = PromptTemplate.from_template("""现在,你是一个真实的人, 请回答用户的问题:

Q: {input}
A:""")

# 使用字符串连接替代PipelinePromptTemplate
combined_prompt = instruction_prompt + "\n\n" + example_prompt + "\n\n" + start_prompt

# 使用RunnableSequence方式
prompt_chain = RunnableSequence(combined_prompt)

# 示例输入
formatted_prompt = prompt_chain.invoke({
    "person": "A",
    "example_q": "你叫什么名字?",
    "example_a": "我叫A",
    "input": "你叫什么名字?"
})

print("使用字符串连接方式:")
print(formatted_prompt)

print("\n" + "="*50 + "\n")

print("使用RunnableSequence方式:")
print(formatted_prompt)
