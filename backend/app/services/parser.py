import csv
from pathlib import Path
from typing import Any

import pandas as pd
from docx import Document
from PyPDF2 import PdfReader


def _dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    df = df.fillna("")
    return df.to_dict(orient="records")


def parse_financial_file(file_path: str) -> dict[str, Any]:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext in {".xlsx", ".xls"}:
        sheets = pd.read_excel(path, sheet_name=None)
        return {"filename": path.name, "type": ext, "content": {k: _dataframe_to_records(v) for k, v in sheets.items()}}

    if ext == ".csv":
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return {"filename": path.name, "type": ext, "content": list(reader)}

    if ext == ".txt":
        text = path.read_text(encoding="utf-8", errors="ignore")
        return {"filename": path.name, "type": ext, "content": text[:200000]}

    if ext == ".docx":
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return {"filename": path.name, "type": ext, "content": text[:200000]}

    if ext == ".pdf":
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            pages.append((page.extract_text() or "").strip())
        return {"filename": path.name, "type": ext, "content": "\n".join(pages)[:200000]}

    raise ValueError(f"Unsupported extension: {ext}")
