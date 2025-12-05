# from .config import settings


async def get_rag_answer(query: str) -> str:
    """
    Placeholder for RAG pipeline.

    Later, this function will:
    1. Split and embed documents
    2. Store / query vector store
    3. Build prompt and call LLM
    """
    # TODO: implement actual RAG pipeline
    # For now, just echo back the query.
    return f"[RAG placeholder] You asked: {query!r}. RAG pipeline is not implemented yet."
