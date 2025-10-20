# ai-research-assistant-starter

A minimal, production‑friendly starter for an **AI Research Assistant**. It wires together:

- **Speech‑to‑Text (ASR)** — Whisper / Faster‑Whisper (GPU if available)
- **Academic Retrieval** — arXiv search with snippet extraction
- **LLM Summarization** — 🤗 Transformers pipeline (default: `facebook/bart-large-cnn`) with safe fallback
- **Text‑to‑Speech (TTS)** — `pyttsx3` (Windows speak) or Piper → WAV on Linux/WSL
- **HTTP API** — FastAPI endpoints: `/ask`, `/status`, `/notion-sync`
- **Sessioning & Logging** — lightweight transcript and structured logs
- **Optional Notion sync** — stub to push transcripts

> Works great on **WSL + CUDA 12.x** (e.g., RTX 4070 SUPER) with Python 3.10 and Conda.  
> On WSL, TTS exports to a WAV file; on native Windows Python, `pyttsx3` can speak directly.

---

## Why this repo

- Clean, interview‑ready structure suitable for pinning on your GitHub profile
- Swappable components (ASR / Retriever / Summarizer / TTS)
- Small, readable codebase with a simple test to validate imports
- No proprietary assets or heavy data included

---

## Quickstart

```bash
# 0) Ensure NVIDIA driver & WSL GPU pass‑through (if using GPU)
nvidia-smi

# 1) Create environment (Python 3.10)
conda create -n research-assistant python=3.10 -y
conda activate research-assistant

# 2) System deps (Whisper needs FFmpeg)
sudo apt-get update && sudo apt-get install -y ffmpeg

# 3) Install Python deps
pip install -r requirements.txt

# 4) Run API
uvicorn app:app --reload --port 8000
```

**Try it**

- Text:
  ```bash
  curl -X POST http://localhost:8000/ask        -H "Content-Type: application/json"        -d '{"query":"Summarize recent advances in retrieval-augmented generation."}'
  ```

- Audio (WAV/MP3):
  ```bash
  curl -X POST "http://localhost:8000/ask" -F "audio_file=@input.wav"
  ```

Response includes: `answer`, `citations` (arXiv IDs), and `tts_wav` (path to WAV file if generated).

---

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

A compact **verification bundle** (script + fixtures) can be shared privately to validate:
- ASR is functional with a sample audio clip (Whisper / Faster‑Whisper)
- Retrieval returns deterministic arXiv results for a fixed query
- Summarizer produces a non‑empty answer within expected latency bounds
- TTS generates a playable WAV file (Linux/WSL) or speaks via `pyttsx3` (Windows)
- API contract: `/ask` responds with `answer`, `citations`, and `tts_wav`

> For reviewers: request the verification pack to reproduce results quickly without exposing private assets.

---

## Notes

- On **WSL**, audio playback is handled by exporting WAV; you can play with `ffplay` or copy to Windows.
- For speed, you may switch the summarizer to a smaller model (e.g., `sshleifer/distilbart-cnn-12-6`).
- Retrieval is abstracted; swap arXiv with your own corpus or a vector database later.

---

## License

MIT
