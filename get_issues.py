import os
import requests
import json
from dotenv import load_dotenv
from time import sleep

# 加载环境变量
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("请在 .env 中设置 GITHUB_TOKEN")

# 配置仓库
OWNER = "CherryHQ"
REPO = "cherry-studio"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


### 可配置起始日期和issues状态
def fetch_all_issues():
    issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
        resp = requests.get(url, headers=HEADERS, params={
            # "since": "2025-07-20T00:00:00+08:00", # 只获取指定日期之后的issues, 东八区
            "state": "all", "per_page": 100, "page": page
        })
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        issues.extend(batch)
        page += 1
        sleep(0.5)
    return issues

def fetch_comments(comments_url):
    comments = []
    page = 1
    while True:
        resp = requests.get(comments_url, headers=HEADERS, params={
            "per_page": 100,
            "page": page
        })
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        comments.extend(batch)
        page += 1
        sleep(0.5)
    return comments

def main():
    raw = fetch_all_issues()
    result = []
    for issue in raw:
        if "pull_request" in issue:
            continue
        item = {
            "number": issue["number"],
            "title": issue.get("title"),
            "body": issue.get("body"),
            "user": issue.get("user", {}).get("login"),
            "labels": [l["name"] for l in issue.get("labels", [])],
            "assignees": [a["login"] for a in issue.get("assignees", [])],
            "state": issue.get("state"),
            "created_at": issue.get("created_at"),
            "updated_at": issue.get("updated_at"),
            "comments": fetch_comments(issue["comments_url"])
        }
        result.append(item)

    with open("repo_s_issues_full.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ 成功保存 {len(result)} 个 issues 到 repo_s_issues_full.json")

if __name__ == "__main__":
    main()
