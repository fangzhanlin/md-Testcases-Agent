import json
import csv

# 文件路径
input_file = 'repo_s_issues_full_.json'
output_file = 'issues_output_final.csv'

# 仓库基础 URL（按你的数据来源设置）
REPO_BASE_URL = 'https://github.com/CherryHQ/cherry-studio/issues/'

# 加载 JSON 数据
with open(input_file, 'r', encoding='utf-8') as f:
    issues = json.load(f)

# 写入 CSV，编码为 utf-8-sig
with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['number', 'url', 'title', 'state', 'created_at', 'labels', 'body']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for issue in issues:
        # 拼接正文和评论
        issue_body = issue.get('body') or ''
        body_parts = [issue_body.strip()]

        for comment in issue.get('comments', []):
            user = comment.get('user', {}).get('login', 'unknown')
            content = comment.get('body', '').strip()
            if content:
                body_parts.append(f"{user}: {content}")
        
        full_body = '\n'.join(body_parts)

        # 【净化步骤 1】替换换行符
        # full_body = full_body.replace('\n', ' | ')

        # 【净化步骤 2 - 新增】替换双引号，防止列合并问题
        # full_body = full_body.replace('"', "'")

        # full_body = full_body.replace('\r', "")
        
        # 对 title 字段也进行净化
        title = issue.get('title', '').replace('"', "'")

        # 组装 URL
        issue_number = issue.get('number')
        issue_url = f"{REPO_BASE_URL}{issue_number}"

        # 提取标签
        raw_labels = issue.get('labels', [])

        if isinstance(raw_labels, list):
            if raw_labels and all(isinstance(label, dict) for label in raw_labels):
                labels = [label.get('name', '') for label in raw_labels]
            else:
                labels = [str(label) for label in raw_labels]
        elif isinstance(raw_labels, str):
            labels = [raw_labels]
        else:
            labels = []

        labels_str = ','.join(labels)

        # 写入行
        writer.writerow({
            'number': issue_number,
            'url': issue_url,
            'title': title, # 使用净化后的 title
            'state': issue.get('state', ''),
            'created_at': issue.get('created_at', ''),
            'labels': labels_str,
            'body': full_body # 使用净化后的 body
        })

print("✅ 所有字段处理完成，CSV 文件保存为:", output_file)