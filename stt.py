import os
import platform
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

_model = None


def _find_ffmpeg() -> str:
    """查找项目内或系统中的 FFmpeg，兼容 Windows、macOS 和 Linux。"""
    executable = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    bundled = BASE_DIR / "bin" / executable
    if bundled.is_file() and os.access(bundled, os.X_OK):
        return str(bundled)

    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    if platform.system() == "Darwin":
        install_hint = "请先执行 `brew install ffmpeg`"
    elif os.name == "nt":
        install_hint = "请安装 FFmpeg 并将其加入 PATH，或放到项目的 bin 目录"
    else:
        install_hint = "请使用系统包管理器安装 FFmpeg"
    raise RuntimeError(f"未找到 FFmpeg，{install_hint}")


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
    command = [
        _find_ffmpeg(), "-y", "-i", input_path,
        "-ar", "16000", "-ac", "1", output_path,
    ]
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        Path(output_path).unlink(missing_ok=True)
        detail = (exc.stderr or "未知错误").strip().splitlines()[-1]
        raise RuntimeError(f"FFmpeg 音频转换失败：{detail}") from exc
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
    try:
        model = _get_model()
        result = model.generate(input=wav_path, batch_size_s=300)
    finally:
        # 模型加载或识别失败时也要清理转换产生的临时文件。
        if wav_path != audio_path:
            Path(wav_path).unlink(missing_ok=True)

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
