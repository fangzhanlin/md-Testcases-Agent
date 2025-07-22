from llm.IssueAbstract import SummarizeLLM
from llm.IssueCheckPic import CheckPicLLM

import asyncio
import pandas as pd


class Workflow:
    def __init__(self, verbose: bool = False):
        # Configuration
        self.verbose = verbose
        self.summarize_llm = SummarizeLLM()
        self.check_pic_llm = CheckPicLLM()

    async def process_row(self, idx, row):
        combined = f"标题：{row['title']}，内容：{row['body']}"
        if self.verbose:
            print(f"正在处理第{idx+1}条：{combined[:50]}...")  # 只打印前50字
        # 并行调用两个LLM
        summarize_task = self.summarize_llm.arun(combined)
        check_pic_task = self.check_pic_llm.arun(combined)
        summary_result, check_pic_result = await asyncio.gather(summarize_task, check_pic_task)
        summary = summary_result["summary"] if summary_result and "summary" in summary_result else ""
        check_pic = check_pic_result["check_pic"] if check_pic_result and "check_pic" in check_pic_result else ""
        return summary, check_pic


async def main():
    df = pd.read_csv("issues_output_final.csv")
    workflow = Workflow(verbose=True)

    tasks = [
        workflow.process_row(idx, row)
        for idx, row in df.iterrows()
    ]
    results = await asyncio.gather(*tasks)

    abstracts, check_pics = zip(*results)
    df["Abstract"] = abstracts
    df["CheckPic"] = check_pics
    df.to_csv("issues_output_final_with_abstract_and_checkpic.csv", index=False, encoding='utf-8-sig')
    print("已保存到 issues_output_final_with_abstract_and_checkpic.csv")


if __name__ == "__main__":
    asyncio.run(main())