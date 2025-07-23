import os
import requests
import json
from dotenv import load_dotenv
import time # 导入 time 模块用于更智能的等待

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

def make_github_request(url, params=None):
    """
    封装 GitHub API 请求，处理速率限制。
    """
    while True:
        resp = requests.get(url, headers=HEADERS, params=params)

        # 检查速率限制信息
        rate_limit_remaining = int(resp.headers.get('X-RateLimit-Remaining', 1))
        rate_limit_reset = int(resp.headers.get('X-RateLimit-Reset', time.time()))

        if resp.status_code == 403 and rate_limit_remaining == 0:
            # 达到速率限制，计算需要等待的时间
            sleep_duration = max(0, rate_limit_reset - time.time()) + 5 # 额外加5秒，确保重置
            print(f"\n⚠️ **达到 GitHub API 速率限制！** 剩余请求: {rate_limit_remaining}。")
            print(f"等待 {sleep_duration:.0f} 秒后重试... (直到 {time.ctime(rate_limit_reset)})")
            time.sleep(sleep_duration)
            continue # 等待结束后重新尝试请求

        resp.raise_for_status() # 对非 2xx 状态码抛出异常
        return resp

### 可配置起始日期和issues状态
def fetch_all_issues():
    issues = []
    page = 1
    print(f"🚀 开始从仓库 '{OWNER}/{REPO}' 获取所有 Issues...")
    while True:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
        params = {
            "state": "all",
            "per_page": 100,
            "page": page
        }
        resp = make_github_request(url, params=params)
        batch = resp.json()

        if not batch:
            print(f"✨ 已获取所有 Issues (共 {len(issues)} 个)。")
            break
        issues.extend(batch)
        print(f"📥 已获取第 {page} 页 Issues，当前总数: {len(issues)}")
        page += 1
        time.sleep(0.5) # 每次请求后稍微暂停，避免不必要的速率限制

    return issues

def fetch_comments(comments_url, issue_number):
    comments = []
    page = 1
    # print(f"    💬 正在获取 Issue #{issue_number} 的评论...")
    while True:
        params = {
            "per_page": 100,
            "page": page
        }
        resp = make_github_request(comments_url, params=params)
        batch = resp.json()

        if not batch:
            # print(f"    ✅ Issue #{issue_number} 评论获取完成。")
            break
        comments.extend(batch)
        # print(f"    -> 已获取 Issue #{issue_number} 第 {page} 页评论，当前数量: {len(comments)}")
        page += 1
        time.sleep(0.2) # 评论请求可以稍微快一点，但仍需等待

    return comments

def main():
    os.makedirs("issues", exist_ok=True)
    raw_issues = fetch_all_issues() # 获取所有 issue 的列表

    total_issues_to_process = 0
    # 先计算需要处理（下载）的实际 issue 数量，以便显示准确进度
    for issue in raw_issues:
        if "pull_request" not in issue: # 排除 Pull Request
            issue_file = f"issues/{issue['number']}.json"
            if not os.path.exists(issue_file):
                total_issues_to_process += 1

    processed_count = 0
    print(f"\n📂 准备处理 {len(raw_issues)} 个 Issues (其中约 {total_issues_to_process} 个需要下载/更新)...")

    for i, issue in enumerate(raw_issues):
        if "pull_request" in issue:
            # print(f"--- 跳过 Pull Request #{issue['number']}")
            continue

        issue_number = issue['number']
        issue_file = f"issues/{issue_number}.json"

        if os.path.exists(issue_file):
            print(f"⏩ {i+1}/{len(raw_issues)} - 跳过已存在 Issue #{issue_number}")
            continue

        processed_count += 1
        print(f"\n--- ⬇️ 正在下载 Issue #{issue_number} ({processed_count}/{total_issues_to_process} - 总进度 {i+1}/{len(raw_issues)}) ---")
        print(f"    标题: {issue.get('title', '无标题')}")

        try:
            item = {
                "number": issue_number,
                "title": issue.get("title"),
                "body": issue.get("body"),
                "user": issue.get("user", {}).get("login"),
                "labels": [l["name"] for l in issue.get("labels", [])],
                "assignees": [a["login"] for a in issue.get("assignees", [])],
                "state": issue.get("state"),
                "created_at": issue.get("created_at"),
                "updated_at": issue.get("updated_at"),
                "comments": fetch_comments(issue["comments_url"], issue_number) # 传递 issue_number 用于反馈
            }

            with open(issue_file, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=2)
            print(f"✅ 成功保存 Issue #{issue_number} 到 {issue_file}")

        except requests.exceptions.RequestException as e:
            print(f"❌ 下载 Issue #{issue_number} 时发生网络错误: {e}")
            print(f"⚠️ 请检查网络连接或稍后重试。该 Issue 已跳过。")
        except Exception as e:
            print(f"❌ 处理 Issue #{issue_number} 时发生未知错误: {e}")
            print(f"⚠️ 该 Issue 已跳过。")

    print(f"\n🎉 所有 Issue 处理完毕！")

if __name__ == "__main__":
    main()