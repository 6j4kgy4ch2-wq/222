import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("/")
async def upload(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="空文件")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件过大")

    saved_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / saved_name
    save_path.write_bytes(content)

    return {"success": True, "filename": saved_name, "original_name": file.filename}


@router.get("/list")
async def list_uploads():
    files = sorted([p.name for p in UPLOAD_DIR.glob("*") if p.is_file()], reverse=True)
    return {"success": True, "files": files}
