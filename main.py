import os
import shutil
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI(title="面试录音助手")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """接收前端上传的音频，调用 fun-asr 转录，返回分段结果。"""
    suffix = Path(audio.filename).suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name

    try:
        import stt
        result = stt.transcribe(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转录失败：{e}")
    finally:
        os.unlink(tmp_path)

    return JSONResponse(result)


@app.post("/api/analyze")
async def analyze(
    segments: str = Form(...),  # JSON 字符串
    company: str = Form(""),
    position: str = Form(""),
):
    """将转录分段发给 DeepSeek 分析，返回分析文本。"""
    import json
    try:
        segs = json.loads(segments)
    except Exception:
        raise HTTPException(status_code=400, detail="segments 格式错误")

    try:
        import analysis
        result = analysis.analyze(segs, company=company, position=position)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败：{e}")

    return JSONResponse({"analysis": result})


@app.post("/api/save")
async def save(
    segments: str = Form(...),
    analysis_text: str = Form(...),
    company: str = Form(""),
    position: str = Form(""),
):
    """保存转录和分析结果到本地 Markdown 文件。"""
    import json
    try:
        segs = json.loads(segments)
    except Exception:
        raise HTTPException(status_code=400, detail="segments 格式错误")

    try:
        import storage
        path = storage.save(segs, analysis_text, company=company, position=position)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败：{e}")

    return JSONResponse({"path": path})


@app.get("/api/records")
def list_records():
    """返回已保存的历史记录列表。"""
    import storage
    return JSONResponse(storage.list_records())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
