from langchain_core.prompts import PromptTemplate

prompt = (
        PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
        + ", 让我开心" +
        "\n 使用{language}语言"
)

print(prompt.invoke({"subject": "机器学习", "language": "中文"}))
print(prompt.invoke({"subject": "机器学习", "language": "中文"}).to_string())
