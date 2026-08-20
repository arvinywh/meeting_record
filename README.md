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

### macOS（Apple Silicon / Intel）

推荐安装 Python 3.11 和 FFmpeg：

```bash
brew install python@3.11 ffmpeg
```

然后在 Finder 中双击 `start.command`，或在终端运行：

```bash
./start.command
```

脚本会在首次运行时创建 `.venv`、安装 Python 依赖、生成 `.env` 并打开浏览器。首次语音转写还会下载 FunASR 模型，需要保持网络连接。macOS 首次录音时，请允许 Safari/Chrome 使用麦克风；如果之前拒绝，可前往“系统设置 → 隐私与安全性 → 麦克风”重新授权。

> 如果尚未安装 Homebrew，请先按照 [brew.sh](https://brew.sh/) 的说明安装。

### 手动安装（Windows / Linux / macOS）

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
```

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

#### 3. 启动服务

```bash
# Windows
start.bat

# Linux / macOS 或直接运行
python3 main.py
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
├── start.command    # macOS 一键启动脚本
├── start.bat        # Windows 启动脚本
├── requirements.txt
└── .env.example
```
