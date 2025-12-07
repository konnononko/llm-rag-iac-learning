from __future__ import annotations

from functools import lru_cache
from typing import Iterable

from openai import OpenAI

from .config import get_settings


@lru_cache
def get_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key)


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    """
    OpenAI Embeddings API でテキスト群をベクトル化するユーティリティ。
    """
    texts_list = list(texts)
    if not texts_list:
        return []

    client = get_client()
    response = client.embeddings.create(
        model=get_settings.openai_embedding_model,
        input=texts_list,
    )

    # OpenAI Python SDK v1系の想定
    return [d.embedding for d in response.data]


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]
