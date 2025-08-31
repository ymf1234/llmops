from langchain_core.prompts import PromptTemplate, PipelinePromptTemplate

full_template = PromptTemplate.from_template(
    """
    {instruction}
    
    {example}
    
    {start}
    """
)

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

pipeline_prompts = [
    ("instruction", instruction_prompt),
    ("example", example_prompt),
    ("start", start_prompt)
]
pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_template,
    pipeline_prompts=pipeline_prompts
)

print(pipeline_prompt.invoke(
    {"person": "机器学习", "example_q": "机器学习是什么", "example_a": "机器学习是一种基于计算机算法的机器学习方法",
     "input": "机器学习是什么?"}).to_string())
