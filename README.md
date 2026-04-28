# 财务慧眼（本地 Ollama Web 版）

这是一个可在本地运行的 WEB 财务报表分析工具：
- 上传 Excel/CSV/PDF/Word/TXT 财务文件
- FastAPI 后端解析文件
- 调用本地 Ollama (`http://127.0.0.1:11434`) 做财务分析
- 页面展示结构化分析结果（JSON）

## 快速启动

### 1) 启动 Ollama
确保本地 Ollama 服务可用，并已拉取模型，例如：
```bash
ollama serve
ollama pull qwen2.5:7b
```

### 2) 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3) 启动系统
```bash
cd ..
./start.sh
```

打开：
- 前端：`http://127.0.0.1:5173`
- 后端文档：`http://127.0.0.1:8000/docs`

## API

- `POST /api/upload/`：上传财务文件
- `GET /api/upload/list`：列出已上传文件
- `POST /api/analyze/`：对指定文件调用 Ollama 分析

请求体示例：
```json
{
  "filename": "d5ec...a2.csv",
  "model": "qwen2.5:7b"
}
```

## 目录

```
backend/
  app/
    api/
      upload.py
      analyze.py
    services/
      parser.py
      ollama_client.py
    config.py
    main.py
frontend/
  index.html
start.sh
```

## 代码打包下载

执行以下命令可将当前项目打包为 ZIP：

```bash
./package_code.sh
```

默认生成文件：`financial-eye-code.zip`（位于项目根目录）。

也可自定义压缩包名称：

```bash
./package_code.sh my-project.zip
```
