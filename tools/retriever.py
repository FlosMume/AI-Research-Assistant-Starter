from typing import List, Tuple
import arxiv
from loguru import logger

def retrieve_arxiv_passages(query: str, k: int = 3) -> Tuple[List[str], List[str]]:
    search = arxiv.Search(
        query=query,
        max_results=k,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    passages, citations = [], []
    for result in search.results():
        abstract = (result.summary or "").strip().replace("\n", " ")
        passages.append(abstract)
        citations.append(f"{result.entry_id}")
        logger.info(f"Retrieved: {result.title} ({result.published.date()})")
    if not passages:
        passages = ["No results found for your query on arXiv."]
        citations = []
    return passages, citations
