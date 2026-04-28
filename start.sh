#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

echo "[1/2] 启动后端 (FastAPI)"
cd "$BACKEND_DIR"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "[2/2] 启动前端静态站点"
cd "$FRONTEND_DIR"
python -m http.server 5173 &
FRONTEND_PID=$!

echo "前端: http://127.0.0.1:5173"
echo "后端: http://127.0.0.1:8000/docs"
echo "按 Ctrl+C 结束"

trap 'kill $BACKEND_PID $FRONTEND_PID' INT TERM
wait
