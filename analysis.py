import os
from openai import OpenAI

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("缺少 DEEPSEEK_API_KEY，请在 .env 中配置")
        _client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    return _client


def _build_transcript_text(segments: list[dict]) -> str:
    if not segments:
        return ""
    lines = []
    for seg in segments:
        lines.append(f"【{seg['speaker']}】{seg['text']}")
    return "\n".join(lines)


def analyze(segments: list[dict], company: str = "", position: str = "") -> str:
    """
    将转录分段发给 DeepSeek，返回面试分析 Markdown 文本。
    """
    transcript = _build_transcript_text(segments)
    context = ""
    if company or position:
        context = f"公司：{company}，岗位：{position}\n\n"

    prompt = f"""你是一位专业的面试教练。以下是一段面试录音的转录记录（带说话人标签）。

{context}转录内容：
{transcript}

请分析这次面试，输出以下内容（使用 Markdown 格式）：

## 面试问题汇总
列出面试官提出的所有主要问题。

## 逐题回答分析
针对每个主要问题，简要评价回答质量（结构是否清晰、内容是否完整、有无亮点或漏洞）。

## 表现亮点
这次面试中回答得好的地方，具体说明。

## 改进建议
具体指出哪些问题的回答可以更好，以及如何改进。

## 总体评分
给这次面试表现打分（1-10 分），并说明理由。
"""

    client = _get_client()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content
