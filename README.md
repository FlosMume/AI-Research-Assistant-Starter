git push -u origin main# ai-research-assistant-starter

An end-to-end multimodal **AI Research Agent** that listens, retrieves, summarizes, and speaks.  
Designed for rapid prototyping, technical demonstration, and job-ready GitHub pinning.

---

## Overview

- Clean structure suitable for pinning on your GitHub profile
- Swappable components (ASR / Retriever / Summarizer / TTS)
- Small, readable codebase with a simple test to validate imports
- No proprietary assets or heavy data included

---

## Quickstart

```bash
# 0) Verify GPU access (optional)
nvidia-smi

# 1) Create environment (Python 3.10)
conda create -n research-assistant python=3.10 -y
conda activate research-assistant

# 2) System deps (Whisper requires FFmpeg)
sudo apt-get update && sudo apt-get install -y ffmpeg

# 3) Install Python deps
pip install -r requirements.txt

# 4) Run API
uvicorn app:app --reload --port 8000


**Try it**

- Text query:
  ```bash
  curl -X POST http://localhost:8000/ask        -H "Content-Type: application/json"        -d '{"query":"Summarize recent advances in retrieval-augmented generation."}'
  ```

- Audio (WAV/MP3) query:
  ```bash
  curl -X POST "http://localhost:8000/ask" -F "audio_file=@input.wav"
  ```

Response includes: `answer`, `citations` (arXiv IDs), and `tts_wav` (path to WAV file if generated).

---

## Agent Architecture

This project functions as a lightweight AI Research Agent, coordinating several cognitive tools through a reasoning loop:

```rust
User → ASR (Whisper/Faster-Whisper) → arXiv Retriever → LLM Summarizer → TTS / Notion Sync
```

Each module operates as an independent agent skill, orchestrated by the FastAPI controller (app.py).
Together they emulate perception (listening), reasoning (retrieval + summarization), and action (text/voice response).

The system can be easily extended with:

Memory (e.g., SQLite or vector store for multi-turn context)

Advanced orchestration using LangChain, LangGraph, or function-calling frameworks

External integrations (Notion, Slack, or custom research APIs)

## Configuration

Edit `.env` (copy from `.env.example`) or set env vars:

- `ASR_BACKEND` = `faster_whisper` | `whisper` | `none`
- `USE_GPU` = `1` or `0`
- `SUMMARIZER_MODEL` = huggingface model id (default: `facebook/bart-large-cnn`)
- Optional Notion: `NOTION_API_KEY`, `NOTION_PAGE_ID`

---

## Project Layout

```
ai-research-assistant-starter/
├─ app.py
├─ config.py
├─ state.py
├─ tools/
│  ├─ asr.py
│  ├─ retriever.py
│  ├─ llm.py
│  ├─ tts.py
│  └─ notion_sync.py
├─ tests/
│  └─ test_smoke.py
├─ cli.py
├─ requirements.txt
├─ environment.yml
├─ .env.example
├─ .gitignore
└─ README.md
```

---

## Technical Verification (available upon request)

A compact **verification bundle** (script + fixtures) can be shared privately to confirm:
- ASR is functional with a reference sample audio clip (Whisper / Faster‑Whisper)
- Retrieval returns deterministic arXiv results for a fixed query
- Summarizer produces a valid non‑empty answer within expected latency bounds
- TTS generates a playable WAV file (Linux/WSL) or speaks via `pyttsx3` (Windows)
- API contract: `/ask` responds with `answer`, `citations`, and `tts_wav`

> For reviewers: request the verification pack to reproduce results quickly without exposing private assets.

---

## Notes

- On WSL, play WAV responses using ffplay or transfer them to Windows for playback.
- Swap in smaller summarizer models (e.g., sshleifer/distilbart-cnn-12-6) for faster inference.
- Retrieval is modular — integrate vector databases (Chroma, FAISS) for richer results.

---

## License

MIT
