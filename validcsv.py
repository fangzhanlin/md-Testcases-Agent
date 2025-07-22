import pandas as pd

def validate_first_column_numeric(csv_file_path):
    """
    从 CSV 文件加载数据到 Pandas DataFrame，并验证第一列（除了标题行）是否都是数字。

    Args:
        csv_file_path (str): CSV 文件的路径。

    Returns:
        bool: 如果第一列（除了标题行）都是数字，则返回 True；否则返回 False。
    """
    try:
        # 加载 CSV 文件到 DataFrame，默认第一行为 header
        df = pd.read_csv(csv_file_path)

        # 检查 DataFrame 是否为空
        if df.empty:
            print(f"Warning: The CSV file '{csv_file_path}' is empty.")
            return True  # 空文件可以认为是满足条件的，因为没有非数字内容

        # 获取第一列的名称（假设它是第一列，并且有标题）
        first_column_name = df.columns[0]

        # 提取第一列的数据，跳过第一行（因为read_csv已经把第一行作为header了）
        # 所以这里df[first_column_name]获取的就是从第二行开始的数据
        first_column_data = df[first_column_name]

        # 尝试将第一列的数据转换为数字类型
        # errors='coerce' 会将无法转换的值设为 NaN
        numeric_column = pd.to_numeric(first_column_data, errors='coerce')

        # 检查转换后的列中是否包含 NaN 值
        # 如果包含 NaN，说明有非数字内容
        if numeric_column.isnull().any():
            print(f"Validation failed: Non-numeric values found in the first column ('{first_column_name}') beyond the header.")
            # 打印出非数字的值和它们的索引，以便调试
            non_numeric_values = first_column_data[numeric_column.isnull()]
            print("Non-numeric entries and their original indices:")
            print(non_numeric_values)
            return False
        else:
            print(f"Validation successful: All values in the first column ('{first_column_name}') beyond the header are numeric.")
            return True

    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return False
    except pd.errors.EmptyDataError:
        print(f"Error: The CSV file '{csv_file_path}' is empty or malformed.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# --- 使用示例 ---
if __name__ == "__main__":
    # 将这里的文件名替换为你的CSV文件
    my_csv_file = 'issues_output_final.csv' 

    print(f"\n--- Validating '{my_csv_file}' ---")
    if validate_first_column_numeric(my_csv_file):
        print("Validation Result: PASSED")
    else:
        print("Validation Result: FAILED")