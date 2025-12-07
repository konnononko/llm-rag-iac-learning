from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from .config import get_settings
from .embeddings import embed_texts, embed_text


@dataclass
class Document:
    id: int    # QdrantのPoint IDとして使う
    text: str
    source: str | None = None    # 元ファイル名など


@lru_cache
def get_qdrant_client() -> QdrantClient:
    # ローカル Docker の Qdrant を想定
    # docker run -p 6333:6333 qdrant/qdrant などで起動
    return QdrantClient(url=get_settings().qdrant_url)


def ensure_collection() -> None:
    client = get_qdrant_client()
    client.recreate_collection(
        collection_name=get_settings().qdrant_collection,
        vectors_config=qmodels.VectorParams(
            size=get_settings().qdrant_vector_size,
            distance=qmodels.Distance.COSINE,
        ),
    )


def index_documents(docs: list[Document]) -> None:
    """
    Docs を埋め込み＋Qdrant に投入する最小実装。
    """
    client = get_qdrant_client()
    settings = get_settings()

    texts = [d.text for d in docs]
    vectors = embed_texts(texts)

    points = []
    for d, v in zip(docs, vectors):
        payload = {"text": d.text}
        if d.source is not None:
            payload["source"] = d.source

        points.append(
            qmodels.PointStruct(
                id=d.id,
                vector=v,
                payload=payload,
            )
        )

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
    )


def search_similar(query: str, limit: int = 4) -> list[str]:
    """
    クエリに近いドキュメントの text を上位 limit 件返す。
    """
    client = get_qdrant_client()
    query_vector = embed_text(query)

    result = client.search(
        collection_name=get_settings().qdrant_collection,
        query_vector=query_vector,
        limit=limit,
        with_payload=True,
    )

    contexts: list[str] = []
    for point in result:
        payload = point.payload or {}
        text = payload.get("text")
        if text:
            contexts.append(text)
    return contexts
