from loguru import logger
from config import settings, torch_device

def _transcribe_with_faster_whisper(audio_bytes: bytes) -> str:
    from faster_whisper import WhisperModel
    import tempfile, soundfile as sf

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        tmp_path = tmp.name

    compute_type = "float16"
    device = "cuda" if torch_device().type == "cuda" else "cpu"
    if device == "cpu":
        compute_type = "int8"

    model = WhisperModel("large-v3", device=device, compute_type=compute_type)
    segments, info = model.transcribe(tmp_path)
    text = " ".join([seg.text for seg in segments])
    logger.info(f"ASR faster-whisper ({device}/{compute_type}) -> {text[:80]}...")
    return text.strip()

def _transcribe_with_openai_whisper(audio_bytes: bytes) -> str:
    import tempfile
    import whisper

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        tmp_path = tmp.name

    device = "cuda" if torch_device().type == "cuda" else "cpu"
    model = whisper.load_model("base", device=device)
    result = model.transcribe(tmp_path)
    text = result.get("text", "").strip()
    logger.info(f"ASR openai-whisper ({device}) -> {text[:80]}...")
    return text

def transcribe_audio(audio_bytes: bytes) -> str:
    backend = settings.ASR_BACKEND.lower()
    if backend == "faster_whisper":
        try:
            return _transcribe_with_faster_whisper(audio_bytes)
        except Exception as e:
            logger.warning(f"faster_whisper failed: {e}; falling back to openai-whisper.")
            return _transcribe_with_openai_whisper(audio_bytes)
    elif backend == "whisper":
        return _transcribe_with_openai_whisper(audio_bytes)
    elif backend == "none":
        return ""
    else:
        logger.warning(f"Unknown ASR_BACKEND={backend}, defaulting to openai-whisper.")
        return _transcribe_with_openai_whisper(audio_bytes)
