from loguru import logger
from config import settings

def sync_to_notion(content: str) -> bool:
    if not (settings.NOTION_API_KEY and settings.NOTION_PAGE_ID):
        logger.info("Notion creds not set; skipping sync.")
        return False
    # TODO: Implement Notion Blocks API call here.
    logger.info(f"[Notion] Would sync {len(content)} chars.")
    return True
