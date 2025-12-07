from __future__ import annotations

from functools import lru_cache

from openai import OpenAI

from .config import get_settings
from .vector_store import search_similar


@lru_cache
def get_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key)


def build_context_prompt(query: str, contexts: list[str]) -> str:
    context_block = "\n\n---\n\n".join(contexts)
    return (
        "You are a helpful assistant for a learning RAG project.\n"
        "Use the following context to answer the question.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {query}"
    )


async def get_rag_answer(query: str) -> str:
    # 類似ドキュメント検索
    contexts = search_similar(query, limit=4)

    # プロンプト構築
    prompt = build_context_prompt(query, contexts)

    # LLM呼び出し
    client = get_client()
    response = client.chat.completions.create(
        model=get_settings().openai_model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=512,
    )

    # 最初の候補の content を返す
    return response.choices[0].message.content or ""
