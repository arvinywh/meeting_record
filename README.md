# Meeting Record

基于 FastAPI + FunASR + DeepSeek 的本地会议录音转写与分析系统。

## 功能

- 上传音频文件，自动语音转文字（STT）
- 使用 DeepSeek 对会议内容进行摘要与分析
- 本地存储转写记录，支持历史查看

## 技术栈

- **后端**：FastAPI + Uvicorn
- **语音识别**：FunASR（本地推理）
- **AI 分析**：DeepSeek API
- **前端**：静态页面（`static/`）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
```

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 3. 启动服务

```bash
# Windows
start.bat

# 或直接运行
python main.py
```

服务默认运行在 `http://localhost:8000`

## 目录结构

```
meeting_record/
├── main.py          # FastAPI 入口
├── stt.py           # 语音转文字模块
├── analysis.py      # AI 分析模块
├── storage.py       # 记录存储模块
├── static/          # 前端静态文件
├── records/         # 转写记录（本地存储）
├── requirements.txt
└── .env.example
```
