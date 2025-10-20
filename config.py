import os
import torch
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)

USE_GPU = os.getenv("USE_GPU", "1") == "1"

def torch_device():
    if USE_GPU and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

def bool_env(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "y")

class Settings:
    ASR_BACKEND = os.getenv("ASR_BACKEND", "faster_whisper")
    SUMMARIZER_MODEL = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
    NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID", "")

settings = Settings()
