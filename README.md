# AI 实习岗位 JD 分析器

这是一个用 Python 编写的命令行工具，用于分析 AI / Agent / Python 后端相关实习岗位 JD。

项目目标是帮助刚入门 Python、准备学习 AI Agent 的同学，通过岗位描述快速了解岗位要求、技术关键词、岗位难度和后续学习方向。

## 功能

- 读取岗位 JD 文本文件
- 提取技术关键词
- 统计文本长度
- 判断岗位难度
- 根据关键词生成学习建议
- 输出 JSON 格式分析结果

## 技术栈

- Python
- pathlib
- sys
- json

## 项目结构

```text
ai-internship-jd-analyzer/
  main.py
  jd.txt
  README.md
  .gitignore