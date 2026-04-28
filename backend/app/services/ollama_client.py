from __future__ import annotations

import json
from typing import Any

import httpx

from ..config import OLLAMA_BASE_URL, OLLAMA_DEFAULT_MODEL


SYSTEM_PROMPT = (
    "你是资深财务分析师。请对用户上传的财务报表内容进行结构化分析，"
    "返回JSON对象，字段包括：summary, key_metrics, risks, fraud_signals, suggestions。"
    "内容必须简洁、可执行，且使用中文。"
)


def build_user_prompt(parsed_payload: dict[str, Any]) -> str:
    compact_payload = json.dumps(parsed_payload, ensure_ascii=False)
    return (
        "请分析下面的财务报表原始数据，并输出严格JSON格式结果。"
        "\n\n数据如下：\n"
        f"{compact_payload}"
    )


async def analyze_with_ollama(parsed_payload: dict[str, Any], model: str | None = None) -> dict[str, Any]:
    model_name = model or OLLAMA_DEFAULT_MODEL
    body = {
        "model": model_name,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(parsed_payload)},
        ],
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=body)
        resp.raise_for_status()
        data = resp.json()

    content = data.get("message", {}).get("content", "{}")
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "summary": "模型返回非JSON，已回退为文本模式。",
            "raw": content,
            "key_metrics": [],
            "risks": [],
            "fraud_signals": [],
            "suggestions": [],
        }
