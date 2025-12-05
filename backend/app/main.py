from fastapi import FastAPI
from .schemas import RAGQuery, RAGResponse
from .rag_pipeline import get_rag_answer

app = FastAPI(
    title="llm-rag-iac-learning",
    description="Learning project for LLM + RAG + IaC",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/rag/query", response_model=RAGResponse)
async def rag_query(payload: RAGQuery) -> RAGResponse:
    answer = await get_rag_answer(payload.query)
    return RAGResponse(answer=answer)
