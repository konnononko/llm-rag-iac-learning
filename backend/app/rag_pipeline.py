from __future__ import annotations

from openai import OpenAI
from .config import get_settings


async def get_rag_answer(query: str) -> str:
    """
    現時点では RAG ではなく、シンプルに LLM に投げるだけの実装。
    後でベクトルDBなどを組み合わせて RAG に拡張する。
    """
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    # OpenAI Chat Completions / Responses API（シンプルな例）
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a learning RAG project."},
            {"role": "user", "content": query},
        ],
        max_tokens=512,
    )

    # 最初の候補の content を返す
    return response.choices[0].message.content or ""
