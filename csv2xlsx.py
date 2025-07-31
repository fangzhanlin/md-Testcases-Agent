import csv
import os
import pandas as pd
from pathlib import Path

def process_csv_content(csv_file_path):
    """
    处理单个CSV文件，返回处理后的数据
    """
    result = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get('filename', '')
                testcases_content = row.get('TestCases', '')
                
                if not testcases_content:
                    continue
                
                # 按<title>分割为多个测试用例（跳过第一个空元素）
                test_cases = [case.strip() for case in testcases_content.split('<title>') if case.strip()]
                
                # 处理每个测试用例
                for case in test_cases:
                    # 初始化各个字段
                    title = ''
                    steps = ''
                    expected_result = ''
                    
                    # 查找<steps>和<result>的位置
                    steps_pos = case.find('<steps>')
                    result_pos = case.find('<result>')
                    
                    if steps_pos != -1 and result_pos != -1:
                        # 三个部分都有
                        title = case[:steps_pos].strip()
                        steps = case[steps_pos + 7:result_pos].strip()  # 7是<steps>的长度
                        expected_result = case[result_pos + 8:].strip()  # 8是<result>的长度
                    elif steps_pos != -1:
                        # 只有title和steps
                        title = case[:steps_pos].strip()
                        steps = case[steps_pos + 7:].strip()
                    elif result_pos != -1:
                        # 只有title和result
                        title = case[:result_pos].strip()
                        expected_result = case[result_pos + 8:].strip()
                    else:
                        # 只有title
                        title = case.strip()
                    
                    # 只添加非空的测试用例
                    if title or steps or expected_result:
                        result.append({
                            '相关文件': filename,
                            '用例标题': title,
                            '用例步骤': steps,
                            '预期结果': expected_result
                        })
    
    except Exception as e:
        print(f"处理文件 {csv_file_path} 时出错: {e}")
    
    return result

def process_folder_csvs(folder_path):
    """
    处理指定文件夹下的所有CSV文件，生成Excel文件
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"文件夹 {folder_path} 不存在")
        return
    
    # 获取所有CSV文件
    csv_files = list(folder_path.glob("*.csv"))
    
    if not csv_files:
        print(f"文件夹 {folder_path} 中没有找到CSV文件")
        return
    
    # 创建Excel文件路径
    excel_file_path = folder_path / f"{folder_path.name}.xlsx"
    
    # 创建ExcelWriter对象
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        for csv_file in csv_files:
            print(f"正在处理: {csv_file.name}")
            
            # 处理CSV文件内容
            processed_data = process_csv_content(csv_file)
            
            if processed_data:
                # 转换为DataFrame
                df = pd.DataFrame(processed_data)
                
                # 使用CSV文件名（不包含扩展名）作为sheet名
                sheet_name = csv_file.stem
                
                # 确保sheet名不超过Excel限制（31字符）
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                
                # 处理Excel中无效的sheet名字符
                invalid_chars = ['\\', '/', '*', '[', ']', ':', '?']
                for char in invalid_chars:
                    sheet_name = sheet_name.replace(char, '_')
                
                # 写入Excel的sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"已创建sheet: {sheet_name}，包含 {len(processed_data)} 条用例")
            else:
                print(f"文件 {csv_file.name} 没有有效数据")
    
    print(f"Excel文件已生成: {excel_file_path}")

# 测试函数，用于验证分割逻辑
def test_parsing():
    test_content = """<title>筛选并添加嵌入模型<steps>1. 打开CherryStudio左侧"模型服务"菜单。
2. 点击"嵌入模型"筛选按钮。
3. 检查只显示嵌入模型类型。
4. 在列表中点击任意模型右侧的"+"按钮添加该模型。
<result>只展示嵌入模型，点击"+"后模型正确添加至"我的模型"，对应按钮状态变化。

<title>嵌入模型搜索功能<steps>1. 打开CherryStudio"模型服务"菜单。
2. 在嵌入模型筛选页面顶部的搜索框输入模型名称或ID（如"bge-m3"）。
3. 检查展示结果。
<result>列表仅展示匹配搜索条件的嵌入模型。"""
    
    # 按<title>分割
    test_cases = [case.strip() for case in test_content.split('<title>') if case.strip()]
    
    for i, case in enumerate(test_cases):
        print(f"\n=== 测试用例 {i+1} ===")
        
        steps_pos = case.find('<steps>')
        result_pos = case.find('<result>')
        
        if steps_pos != -1 and result_pos != -1:
            title = case[:steps_pos].strip()
            steps = case[steps_pos + 7:result_pos].strip()
            expected_result = case[result_pos + 8:].strip()
            
            print(f"用例标题: {title}")
            print(f"用例步骤: {steps}")
            print(f"预期结果: {expected_result}")

if __name__ == '__main__':
    # 可以先测试分割逻辑
    print("测试分割逻辑：")
    test_parsing()
    
    print("\n" + "="*50)
    print("开始处理文件夹：")
    
    # 指定要处理的文件夹
    folder_name = "cherry-docs-modules"
    process_folder_csvs(folder_name)
