# AI 实习岗位 JD 分析器

这是一个基于 Python 的 AI 实习岗位 JD 分析工具。

项目可以读取岗位 JD 文本，支持规则分析和大模型分析两种模式，并可以将分析结果保存到 SQLite 数据库中，方便后续查看历史记录。

## 功能

- 读取岗位 JD 文本文件
- 规则版关键词提取
- 规则版岗位难度判断
- 规则版学习建议生成
- LLM 智能分析岗位 JD
- 输出结构化 JSON
- 保存分析记录到 SQLite
- 查看历史分析记录
- 使用 `.env` 管理 API Key

## 技术栈

- Python
- OpenAI-compatible API
- SQLite
- python-dotenv
- JSON
- Git / GitHub

## 项目结构

```text
ai-internship-jd-analyzer/
  main.py
  llm_service.py
  config.py
  db.py
  jd.txt
  README.md
  requirements.txt
  .env.example
  .gitignore
```

本地运行时还会生成：

```text
.env
.venv/
app.db
```

这些文件不会上传到 GitHub。

## 环境变量配置

项目使用 `.env` 文件保存 API 配置。

先复制 `.env.example`，创建 `.env`：

```env
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://your-api-base-url/v1
```

注意：`.env` 里包含真实 API Key，不要上传到 GitHub。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 规则分析

```bash
python main.py jd.txt
```

或者：

```bash
python main.py jd.txt --rule
```

### LLM 分析

```bash
python main.py jd.txt --llm
```

### 保存规则分析记录

```bash
python main.py jd.txt --rule --save
```

### 保存 LLM 分析记录

```bash
python main.py jd.txt --llm --save
```

### 查看历史记录

```bash
python main.py --history
```

## 示例 JD

```text
我们正在招聘 AI Agent 实习生，要求熟悉 Python，了解 FastAPI 和大模型 API 调用。
加分项包括 RAG、LangChain、LangGraph、向量数据库、Function Calling 和 Docker。
```

## 示例输出

```json
{
  "mode": "llm",
  "result": {
    "role_type": "AI Agent 实习生",
    "required_skills": [
      "Python",
      "FastAPI",
      "大模型 API 调用"
    ],
    "bonus_skills": [
      "RAG",
      "LangChain",
      "LangGraph",
      "向量数据库",
      "Function Calling",
      "Docker"
    ],
    "difficulty": "适合有一定基础的初学者",
    "learning_suggestions": [
      "加强 Python 工程化能力",
      "学习 FastAPI 接口开发",
      "学习 RAG 和向量数据库基础"
    ],
    "interview_questions": [
      "什么是 RAG？",
      "Function Calling 是什么？",
      "Agent 和普通聊天机器人有什么区别？"
    ]
  }
}
```

## 当前版本说明

当前版本是命令行工具，支持规则分析、LLM 分析、结果保存和历史记录查看。

## 后续计划

- 使用 FastAPI 封装为后端接口
- 支持上传多个 JD 批量分析
- 增加简历和 JD 匹配功能
- 接入 RAG，用于岗位知识库检索
- 使用 LangChain / LangGraph 实现求职助手 Agent
- 尝试接入 MCP 工具调用能力
## FastAPI 接口版本

项目支持使用 FastAPI 启动后端服务。

启动方式：

```bash
uvicorn app:app --reload
启动后打开http://127.0.0.1:8000/docs