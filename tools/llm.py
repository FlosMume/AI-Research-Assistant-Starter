from typing import List
from loguru import logger
from config import settings, torch_device

def _transformers_summary(prompt: str, passages: List[str]) -> str:
    from transformers import pipeline
    device = 0 if torch_device().type == "cuda" else -1
    text = "\n\n".join(passages)[:4000]
    summarizer = pipeline("summarization", model=settings.SUMMARIZER_MODEL, device=device)
    out = summarizer(text, max_length=220, min_length=80, do_sample=False)
    return out[0]["summary_text"]

def _fallback_extractive(passages: List[str]) -> str:
    text = " ".join(passages)
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(sentences[:4])[:1500]

def summarize_passages(prompt: str, passages: List[str]) -> str:
    try:
        summary = _transformers_summary(prompt, passages)
        logger.info("Summarization via transformers ✅")
        return summary
    except Exception as e:
        logger.warning(f"Transformers summarization failed: {e}; using fallback.")
        return _fallback_extractive(passages)
