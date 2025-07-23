import os
import asyncio
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import glob

load_dotenv(find_dotenv())

DEFAULT_OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-mini")
DEFAULT_OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE_HIGH", 0.7))

class SummarizeLLM:
    def __init__(self):
        self.llm = ChatOpenAI(model=DEFAULT_OPENAI_MODEL_NAME, temperature=DEFAULT_OPENAI_TEMPERATURE)
        self.output_parser = self.get_output_parser()
        self.prompt = self.get_prompt()
        self.chain = self.get_chain()

    def get_output_parser(self):
        response_schemas = [
            ResponseSchema(name="testcases", description="详细的多个测试用例", type="string")
        ]
        return StructuredOutputParser.from_response_schemas(response_schemas)

    def get_prompt(self):
        human_template = """
        <format_instructions>{format_instructions}</format_instructions>
        <task>
        <goal>
        请基于下面的功能说明文档尽可能详细地列举和编写测试用例, 以确保文档中的所有功能能正常使用.

        <paragraph>{paragraph}</paragraph>
        </goal>

        <example>
        发送信息|选择某个模型，尝试所有的参数组合（主要是输入框和助手设置切换），发起对话，查看网络请求和渲染到页面的是否一致~选择模型|点击选择模型设置界面的下拉框, 确保可以选择所有可用模型~
        </example>

        <constraints>
        1. 必须使用简体中文.
        2. 每个测试用例应该有一个标题, 描述这个用例涉及的功能点, 和后文用|隔开.
        3. 尽量列举所有可能的测试用例, 多个用例间用~隔开.
        4. 用例必须尽可能详细, 比如说'安装服务'应该要写'MCP的安装服务', 不能省略.
        5. 不允许有幻觉, 绝对不能提到文档不存在的内容!
        </constraints>
        </task>
        


        """
        human_message = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([human_message])
        return chat_prompt.partial(
            format_instructions=self.output_parser.get_format_instructions(),
        )

    def get_chain(self):
        return self.prompt | self.llm | self.output_parser

    async def arun(self, paragraph: str):
        try:
            return await self.chain.ainvoke({"paragraph": paragraph})
        except Exception as e:
            print(f"Error: {e}")
            return None

async def main():
    # 读取CSV文件
    folder = "test_md"  # 指定你的md文件夹路径
    md_files = glob.glob(os.path.join(folder, "*.md"))
    summarize_llm = SummarizeLLM()
    results = []

    for idx, md_path in enumerate(md_files):
        with open(md_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        print(f"正在处理第{idx+1}个文件：{os.path.basename(md_path)}")
        result = await summarize_llm.arun(content)
        testcases = result["testcases"] if result and "testcases" in result else ""
        results.append({"filename": os.path.basename(md_path), "TestCases": testcases})

    df = pd.DataFrame(results)
    df.to_csv("md_testcases_output.csv", index=False, encoding='utf-8-sig')
    print("已保存到 md_testcases_output.csv")

if __name__ == "__main__":
    asyncio.run(main())