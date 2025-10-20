from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from loguru import logger

from config import settings
from state import current_session
from tools.asr import transcribe_audio
from tools.retriever import retrieve_arxiv_passages
from tools.llm import summarize_passages
from tools.tts import speak_or_save
from tools.notion_sync import sync_to_notion

app = FastAPI(title="AI Research Assistant")

class AskText(BaseModel):
    query: str

@app.get("/status")
def status():
    return {"status": "ok", "session_id": current_session.session_id}

@app.post("/ask")
async def ask_text_or_audio(
    query: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None)
):
    try:
        if not query and not audio_file:
            raise HTTPException(status_code=400, detail="Provide text 'query' or 'audio_file'.")

        if audio_file:
            audio_bytes = await audio_file.read()
            query = transcribe_audio(audio_bytes)
            current_session.add("user", f"[audio] {query}", source="audio")
        else:
            current_session.add("user", query, source="text")

        passages, citations = retrieve_arxiv_passages(query)
        answer = summarize_passages(query, passages)
        wav_path = speak_or_save(answer)

        current_session.add("assistant", answer, citations=citations, tts=wav_path)

        return JSONResponse({
            "session_id": current_session.session_id,
            "query": query,
            "answer": answer,
            "citations": citations,
            "tts_wav": wav_path
        })
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

class NotionPayload(BaseModel):
    content: Optional[str] = None

@app.post("/notion-sync")
def notion_sync(payload: NotionPayload):
    try:
        text = payload.content or "\n".join(
            [f"{t.role.upper()}: {t.content}" for t in current_session.turns]
        )
        ok = sync_to_notion(text)
        return {"ok": ok}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
