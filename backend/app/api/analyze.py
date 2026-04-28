from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..config import UPLOAD_DIR
from ..services.ollama_client import analyze_with_ollama
from ..services.parser import parse_financial_file

router = APIRouter(prefix="/api/analyze", tags=["analyze"])


class AnalyzeRequest(BaseModel):
    filename: str
    model: str | None = None


@router.post("/")
async def analyze(req: AnalyzeRequest):
    file_path = (UPLOAD_DIR / req.filename).resolve()
    if not file_path.exists() or UPLOAD_DIR.resolve() not in file_path.parents:
        raise HTTPException(status_code=404, detail="文件不存在")

    try:
        parsed = parse_financial_file(str(file_path))
        result = await analyze_with_ollama(parsed, req.model)
        return {"success": True, "filename": req.filename, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {e}") from e
