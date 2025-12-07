from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from .config import get_settings


_settings = get_settings()
_client = OpenAI(api_key=_settings.openai_api_key)


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    """
    OpenAI Embeddings API でテキスト群をベクトル化するユーティリティ。
    """
    texts_list = list(texts)
    if not texts_list:
        return []

    response = _client.embeddings.create(
        model=_settings.openai_embedding_model,
        input=texts_list,
    )

    # OpenAI Python SDK v1系の想定
    return [d.embedding for d in response.data]


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]
