from llm.IssueAbstract import SummarizeLLM
from llm.IssueCheckPic import CheckPicLLM

import asyncio
import pandas as pd

class Workflow:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        # 注册所有LLM功能，key为输出列名，value为LLM实例和结果key
        self.llms = [
            {"name": "Abstract", "llm": SummarizeLLM(), "result_key": "summary"},
            {"name": "CheckPic", "llm": CheckPicLLM(), "result_key": "check_pic"},
            # 未来可在此添加更多LLM
            # {"name": "NewFeature", "llm": NewLLM(), "result_key": "new_feature"},
        ]

    async def process_row(self, idx, row):
        combined = f"标题：{row['title']}，内容：{row['body']}"
        if self.verbose:
            print(f"正在处理第{idx+1}条：{combined[:50]}...")
        # 并行调用所有LLM
        tasks = [item["llm"].arun(combined) for item in self.llms]
        results = await asyncio.gather(*tasks)
        # 提取每个LLM的结果
        row_results = []
        for item, result in zip(self.llms, results):
            value = result.get(item["result_key"], "") if result else ""
            row_results.append(value)
        return row_results

async def main():
    df = pd.read_csv("issues_output_final.csv")
    workflow = Workflow(verbose=True)
    tasks = [
        workflow.process_row(idx, row)
        for idx, row in df.iterrows()
    ]
    results = await asyncio.gather(*tasks)
    # 拆分结果并写入DataFrame
    for i, item in enumerate(workflow.llms):
        df[item["name"]] = [row[i] for row in results]
    df.to_csv("issues_output_final_with_abstract_and_checkpic.csv", index=False, encoding='utf-8-sig')
    print("已保存到 issues_output_final_with_abstract_and_checkpic.csv")

if __name__ == "__main__":
    asyncio.run(main())