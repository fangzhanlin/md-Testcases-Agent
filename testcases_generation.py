import os
import json
import asyncio
import pandas as pd
import re
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.schema import HumanMessage
import glob
from pathlib import Path

load_dotenv(find_dotenv())

DEFAULT_OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1")  # 确保使用支持视觉的模型
DEFAULT_OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE_HIGH", 0.7))

class SummarizeLLM:
    def __init__(self):
        self.llm = ChatOpenAI(model=DEFAULT_OPENAI_MODEL_NAME, temperature=DEFAULT_OPENAI_TEMPERATURE)
        self.output_parser = self.get_output_parser()

    def get_output_parser(self):
        response_schemas = [
            ResponseSchema(name="testcases", description="详细的多个测试用例", type="string")
        ]
        return StructuredOutputParser.from_response_schemas(response_schemas)

    def extract_image_paths(self, content):
        """提取md文件中的图片路径"""
        # 匹配 <img src="../../.gitbook/assets/xxx" 格式
        img_pattern = r'<img\s+src="([^"]*\.gitbook/assets/[^"]+)"'
        matches = re.findall(img_pattern, content)
        
        image_urls = []
        for match in matches:
            # 从.gitbook开始截取路径
            gitbook_index = match.find('.gitbook')
            if gitbook_index != -1:
                relative_path = match[gitbook_index:]
                full_url = f"https://raw.githubusercontent.com/CherryHQ/cherry-studio-docs/main/{relative_path}"
                image_urls.append(full_url)
        
        return image_urls

    def clean_content_for_text(self, content):
        """清理内容，移除图片标签但保留figcaption文本"""
        # 替换figure标签，保留figcaption中的文本
        figure_pattern = r'<figure><img[^>]*><figcaption><p>([^<]*)</p></figcaption></figure>'
        content = re.sub(figure_pattern, r'[图片：\1]', content)
        
        # 移除其他可能的img标签
        content = re.sub(r'<img[^>]*>', '[图片]', content)
        
        return content

    async def arun(self, paragraph: str):
        try:
            # 提取图片URL
            image_urls = self.extract_image_paths(paragraph)
            
            # 清理文本内容
            clean_text = self.clean_content_for_text(paragraph)
            
            # 构建消息内容
            message_content = []
            
            # 添加文本部分
            text_prompt = f"""
            <format_instructions>{self.get_output_parser().get_format_instructions()}</format_instructions>
            <task>
            <goal>
            请基于下面的功能说明和图片说明，尽可能详细地列举和编写测试用例, 包含：标题，操作步骤 (输入输出等)和预期结果. 确保测试用例覆盖文档和图片中涉及的所有功能和模块的正常使用.

            <paragraph>{clean_text}</paragraph>
            </goal>

            <example>
            <title>筛选嵌入模型并添加模型<steps>1. 打开CherryStudio左侧“模型服务”菜单。\n2. 点击“嵌入模型”筛选按钮。\n3. 检查只显示嵌入模型类型。\n4. 在列表中点击任意模型右侧的“+”按钮添加该模型。\n<result>列表正确筛选，仅展示嵌入模型，点击“+”后模型成功添加至“我的模型”。\n<title>知识库入口访问和页面加载<steps>1. 打开CherryStudio主界面。\n2. 在左侧工具栏点击知识库图标。\n3. 检查是否进入知识库管理页面，显示“暂无知识库”及“添加”按钮。\n<result>点击知识库图标后能正常访问知识库管理页面，页面元素显示完整。\n
            </example>

            <constraints>
            1. 必须使用中文.
            2. 每个测试用例应该有一个标题, 描述这个用例涉及的功能点, 用<title>开始.
            3. 尽量列举所有可能的测试用例, 用例步骤用<steps>开始.
            4. 预期结果用<result>开始.
            5. 用例必须尽可能详细, 不能简单写'安装服务'，应该要写'filesystem mcp server的安装服务', 不能省略.
            6. 不允许有幻觉, 绝对不能提到文档不存在的内容!
            7. 如果有图片，请结合图片内容理解功能并生成相应的测试用例.
            </constraints>
            </task>
            """
            
            message_content.append({"type": "text", "text": text_prompt})
            
            # 添加图片部分
            for image_url in image_urls:
                message_content.append({"type": "image_url", "image_url": {"url": image_url}})
            
            # 创建消息
            message = HumanMessage(content=message_content)
            
            # 调用模型
            response = await self.llm.ainvoke([message])
            
            # 解析响应
            parsed_response = self.output_parser.parse(response.content)
            return parsed_response
            
        except Exception as e:
            print(f"Error: {e}")
            return None

def find_all_md_files(root_folder):
    """递归查找所有子文件夹中的md文件"""
    md_files = []
    root_path = Path(root_folder)
    
    # 遍历所有子文件夹
    for subfolder in root_path.iterdir():
        if subfolder.is_dir():
            # 在每个子文件夹中查找md文件
            for md_file in subfolder.glob("*.md"):
                md_files.append({
                    'file_path': md_file,
                    'subfolder': subfolder.name,
                    'filename': md_file.stem  # 不包含扩展名的文件名
                })
    
    return md_files

async def process_md_file(md_info, summarize_llm):
    """处理单个md文件"""
    file_path = md_info['file_path']
    json_path = file_path.with_suffix('.json')
    
    # 如果json文件已存在，跳过处理
    if json_path.exists():
        print(f"  JSON文件已存在，跳过: {json_path.name}")
        return json_path
    
    # 读取md文件内容
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
    except Exception as e:
        print(f"  读取文件失败: {file_path}, 错误: {e}")
        return None
    
    print(f"  正在处理: {file_path.name}")
    
    # 检查是否有图片
    image_urls = summarize_llm.extract_image_paths(content)
    if image_urls:
        print(f"    发现 {len(image_urls)} 张图片")
    
    # 调用LLM处理
    result = await summarize_llm.arun(content)
    
    if result:
        # 构建要保存的数据
        json_data = {
            "filename": file_path.name,
            "subfolder": md_info['subfolder'],
            "testcases": result.get("testcases", ""),
            "images_count": len(image_urls),
            "image_urls": image_urls
        }
        
        # 保存为JSON文件
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"    已保存JSON: {json_path.name}")
            return json_path
        except Exception as e:
            print(f"    保存JSON失败: {e}")
            return None
    else:
        print(f"    LLM处理失败")
        return None

def collect_json_files_by_subfolder(root_folder):
    """按子文件夹收集所有JSON文件"""
    root_path = Path(root_folder)
    subfolder_json_map = {}
    
    for subfolder in root_path.iterdir():
        if subfolder.is_dir():
            json_files = list(subfolder.glob("*.json"))
            if json_files:
                subfolder_json_map[subfolder.name] = json_files
    
    return subfolder_json_map

def create_csv_for_subfolder(subfolder_name, json_files, root_folder):
    """为指定子文件夹创建CSV文件"""
    results = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            results.append({
                "filename": data.get("filename", json_file.stem + ".md"),
                "TestCases": data.get("testcases", ""),
                "images_count": data.get("images_count", 0)
            })
        except Exception as e:
            print(f"读取JSON文件失败: {json_file}, 错误: {e}")
            continue
    
    if results:
        df = pd.DataFrame(results)
        csv_path = Path(root_folder) / f"{subfolder_name}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"已创建CSV文件: {csv_path}")
        return csv_path
    else:
        print(f"子文件夹 {subfolder_name} 没有有效的数据生成CSV")
        return None

async def main():
    root_folder = "cherry-docs-modules"  # 指定你的根文件夹路径
    
    if not os.path.exists(root_folder):
        print(f"文件夹不存在: {root_folder}")
        return
    
    print(f"开始处理文件夹: {root_folder}")
    
    # 查找所有md文件
    md_files = find_all_md_files(root_folder)
    
    if not md_files:
        print("未找到任何md文件")
        return
    
    print(f"找到 {len(md_files)} 个md文件")
    
    # 按子文件夹分组
    subfolders = {}
    for md_info in md_files:
        subfolder = md_info['subfolder']
        if subfolder not in subfolders:
            subfolders[subfolder] = []
        subfolders[subfolder].append(md_info)
    
    print(f"涉及 {len(subfolders)} 个子文件夹: {list(subfolders.keys())}")
    
    # 初始化LLM
    summarize_llm = SummarizeLLM()
    
    # 处理每个子文件夹的md文件
    for subfolder_name, md_files_in_subfolder in subfolders.items():
        print(f"\n处理子文件夹: {subfolder_name} ({len(md_files_in_subfolder)} 个文件)")
        
        for md_info in md_files_in_subfolder:
            await process_md_file(md_info, summarize_llm)
    
    print(f"\n所有md文件处理完成，开始生成CSV文件...")
    
    # 收集所有JSON文件并生成CSV
    subfolder_json_map = collect_json_files_by_subfolder(root_folder)
    
    for subfolder_name, json_files in subfolder_json_map.items():
        print(f"\n为子文件夹 {subfolder_name} 生成CSV ({len(json_files)} 个JSON文件)")
        create_csv_for_subfolder(subfolder_name, json_files, root_folder)
    
    print(f"\n所有任务完成！")

if __name__ == "__main__":
    asyncio.run(main())
