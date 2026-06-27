import re
from datetime import datetime
from pathlib import Path

RECORDS_DIR = Path(__file__).parent / "records"


def _safe_filename(text: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", text).strip() or "未命名"


def save(
    segments: list[dict],
    analysis: str,
    company: str = "",
    position: str = "",
) -> str:
    """
    将转录和分析结果保存为 Markdown 文件。
    返回保存的文件路径。
    """
    RECORDS_DIR.mkdir(exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H%M")
    company_part = _safe_filename(company) if company else "未知公司"
    position_part = _safe_filename(position) if position else ""
    name_part = f"{company_part}_{position_part}" if position_part else company_part
    filename = f"{date_str}_{time_str}_{name_part}.md"
    filepath = RECORDS_DIR / filename

    title = company_part
    if position_part:
        title += f" · {position_part}"

    transcript_md = "\n\n".join(
        f"**{seg['speaker']}**：{seg['text']}" for seg in segments
    )
    if not transcript_md:
        transcript_md = "（无转录内容）"

    content = f"""# {title} 面试记录

> 日期：{datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 转录原文

{transcript_md}

---

## DeepSeek 面试分析

{analysis}
"""

    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def list_records() -> list[dict]:
    """返回所有已保存记录的文件名和路径列表。"""
    RECORDS_DIR.mkdir(exist_ok=True)
    files = sorted(RECORDS_DIR.glob("*.md"), reverse=True)
    return [{"name": f.stem, "path": str(f)} for f in files]
