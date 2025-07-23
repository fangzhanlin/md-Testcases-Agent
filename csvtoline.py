import csv

def process_csv(input_file, output_file):
    # 读取csv文件，拼接TestCases列内容，并保留filename
    result = []
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            testcases_content = row['TestCases']
            # 按~分割为多行
            lines = [line.strip() for line in testcases_content.split('~') if line.strip()]
            # 处理每一行，按|分割为标题和内容
            for line in lines:
                if '|' in line:
                    title, content = line.split('|', 1)
                    result.append({'filename': filename, '标题': title.strip(), '内容': content.strip()})
                else:
                    result.append({'filename': filename, '标题': '', '内容': line.strip()})

    # 写入新的csv文件
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', '标题', '内容'])
        writer.writeheader()
        writer.writerows(result)

if __name__ == '__main__':
    # 示例用法
    process_csv('md_testcases_output.csv', 'output.csv')