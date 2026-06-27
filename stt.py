import os
import subprocess
from pathlib import Path

# 优先使用项目 bin 目录内的 ffmpeg，避免依赖系统 PATH
_FFMPEG = str(Path(__file__).parent / "bin" / "ffmpeg.exe")
if not Path(_FFMPEG).exists():
    _FFMPEG = "ffmpeg"  # 回退到系统 PATH

_model = None


def _get_model():
    global _model
    if _model is None:
        from funasr import AutoModel
        _model = AutoModel(
            model="paraformer-zh",
            vad_model="fsmn-vad",
            punc_model="ct-punc",
            spk_model="cam++",
            hub="ms",  # ModelScope，国内下载更快
        )
    return _model


def _to_wav(input_path: str) -> str:
    """将任意音频格式转换为 WAV，funasr 识别更稳定。"""
    output_path = str(Path(input_path).with_suffix(".wav"))
    if input_path == output_path:
        return output_path
    subprocess.run(
        [_FFMPEG, "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_path


def transcribe(audio_path: str) -> dict:
    """
    转录音频文件，返回带说话人标签的分段列表。

    返回格式：
    {
        "full_text": "完整转录文字...",
        "segments": [
            {"speaker": "说话人A", "start_ms": 0, "end_ms": 3000, "text": "你好"},
            ...
        ]
    }
    """
    wav_path = _to_wav(audio_path)
    model = _get_model()

    result = model.generate(input=wav_path, batch_size_s=300)

    # 清理临时 wav（如果是转换来的）
    if wav_path != audio_path and os.path.exists(wav_path):
        os.remove(wav_path)

    if not result:
        return {"full_text": "", "segments": []}

    res = result[0]
    full_text = res.get("text", "")

    # sentence_info 包含按句子分段的说话人信息
    sentence_info = res.get("sentence_info", [])
    segments = []
    speaker_map: dict[int, str] = {}  # 数字 ID → 说话人A/B/C

    for item in sentence_info:
        spk_id = item.get("spk", 0)
        if spk_id not in speaker_map:
            label = chr(ord("A") + len(speaker_map))  # 0→A, 1→B, 2→C...
            speaker_map[spk_id] = f"说话人{label}"
        segments.append(
            {
                "speaker": speaker_map[spk_id],
                "start_ms": item.get("start", 0),
                "end_ms": item.get("end", 0),
                "text": item.get("text", ""),
            }
        )

    return {"full_text": full_text, "segments": segments}
