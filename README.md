# 基于产品文档生成测试用例文档

能够基于GitHub仓库产品文档生成测试用例内容。

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

## 针对文件夹生成测试用例
```bash
uv run .\testcases_generation.py
```

## csv汇总为xlsx
```bash
uv run .\csv2xlsx.py
```

## xlsx格式生成
```bash
uv run xlsx_formatting.py
```
