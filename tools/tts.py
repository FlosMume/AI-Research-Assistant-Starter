import os
import subprocess
from loguru import logger
from sys import platform

def _pyttsx3_speak(text: str) -> str:
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return ""
    except Exception as e:
        logger.warning(f"pyttsx3 speak failed: {e}")
        return ""

def _piper_to_wav(text: str, wav_out: str) -> str:
    model = os.getenv("PIPER_MODEL", "")
    if not model:
        raise RuntimeError("PIPER_MODEL not set; cannot TTS with piper.")
    cmd = ["piper", "-m", model, "-f", wav_out]
    p = subprocess.run(cmd, input=text.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(f"piper failed: {p.stderr.decode('utf-8')}")
    return wav_out

def speak_or_save(text: str) -> str:
    if platform.startswith("win"):
        _pyttsx3_speak(text)
        return ""
    wav_out = "/tmp/ai_assistant_reply.wav"
    try:
        return _piper_to_wav(text, wav_out)
    except Exception as e:
        logger.warning(f"Piper TTS failed/unavailable: {e}. No audio generated.")
        return ""
