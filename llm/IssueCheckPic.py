import os
import asyncio
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv(find_dotenv())

DEFAULT_OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-mini")
DEFAULT_OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE_HIGH", 0.7))

class CheckPicLLM:
    def __init__(self):
        self.llm = ChatOpenAI(model=DEFAULT_OPENAI_MODEL_NAME, temperature=DEFAULT_OPENAI_TEMPERATURE)
        self.output_parser = self.get_output_parser()
        self.prompt = self.get_prompt()
        self.chain = self.get_chain()

    def get_output_parser(self):
        response_schemas = [
            ResponseSchema(name="check_pic", description="需要图片检查为Yes，否则为No", type="string")
        ]
        return StructuredOutputParser.from_response_schemas(response_schemas)

    def get_prompt(self):
        human_template = """
        <format_instructions>{format_instructions}</format_instructions>
        <task>
        请对下面的段落进行分析，如果发现缺少的图片对总结非常非常重要，回答Yes，否则回答No。
        </task>
        <paragraph>{paragraph}</paragraph>
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
    df = pd.read_csv("issues_output_final.csv")
    check_pic_results = []
    check_pic_llm = CheckPicLLM()

    for idx, row in df.iterrows():
        combined = f"标题：{row['title']}，内容：{row['body']}"
        print(f"正在处理第{idx+1}条：{combined[:50]}...")  # 只打印前50字
        result = await check_pic_llm.arun(combined)
        if result and "check_pic" in result:
            check_pic_results.append(result["check_pic"])
        else:
            check_pic_results.append("")

    df["CheckPic"] = check_pic_results
    df.to_csv("issues_output_final_with_checkpic.csv", index=False, encoding='utf-8-sig')
    print("已保存到 issues_output_final_with_checkpic.csv")

if __name__ == "__main__":
    asyncio.run(main())