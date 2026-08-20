#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

find_python() {
  local candidate
  for candidate in python3.11 python3.12 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c \
      'import sys; raise SystemExit(not ((3, 10) <= sys.version_info[:2] <= (3, 12)))'; then
      command -v "$candidate"
      return 0
    fi
  done
  return 1
}

if ! PYTHON_BIN="$(find_python)"; then
  echo "需要 Python 3.10–3.12（推荐 3.11）。"
  echo "请先安装：brew install python@3.11"
  read -r -p "按回车键退出..."
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1 && [ ! -x "bin/ffmpeg" ]; then
  echo "未找到 FFmpeg。请先安装：brew install ffmpeg"
  read -r -p "按回车键退出..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "首次运行：正在创建 Python 虚拟环境..."
  "$PYTHON_BIN" -m venv .venv
fi

if ! .venv/bin/python -c 'import fastapi, funasr, openai, uvicorn' >/dev/null 2>&1; then
  echo "首次运行：正在安装项目依赖，这可能需要几分钟..."
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -r requirements.txt
fi

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "已创建 .env。使用 DeepSeek 分析前，请填写 DEEPSEEK_API_KEY。"
fi

echo "Meeting Record 启动于 http://127.0.0.1:8000"
(sleep 2; open "http://127.0.0.1:8000") &
exec .venv/bin/python main.py
