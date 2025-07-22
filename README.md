# Issues整理

为大型热门项目总结issues内容、归类所属功能模块、构建测试用例等。

## 🛠️ 安装要求

- Python 3.12 或更高版本
- [uv](https://github.com/astral-sh/uv) 包管理工具

> 
> ## On Windows.
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> 

## 使用 uv 创建虚拟环境并安装依赖
```bash
uv venv .venv
uv sync
```

## 基本用法, 获取指定issues
```bash
uv run .\get_issues.py
```

## json转换为csv (适应表格显示)
```bash
uv run .\issues_jsontocsv.py
```

## 并行生成
```bash
uv run workflow.py
```
