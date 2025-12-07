from __future__ import annotations

from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from .config import get_settings
from .embeddings import embed_texts, embed_text


@dataclass
class Document:
    id: str
    text: str


_settings = get_settings()


def get_qdrant_client() -> QdrantClient:
    # ローカル Docker の Qdrant を想定
    # docker run -p 6333:6333 qdrant/qdrant などで起動
    return QdrantClient(url=_settings.qdrant_url)


def ensure_collection() -> None:
    client = get_qdrant_client()
    client.recreate_collection(
        collection_name=_settings.qdrant_collection,
        vectors_config=qmodels.VectorParams(
            size=_settings.qdrant_vector_size,
            distance=qmodels.Distance.COSINE,
        ),
    )


def index_documents(docs: list[Document]) -> None:
    """
    Docs を埋め込み＋Qdrant に投入する最小実装。
    """
    client = get_qdrant_client()
    texts = [d.text for d in docs]
    vectors = embed_texts(texts)

    client.upsert(
        collection_name=_settings.qdrant_collection,
        points=[
            qmodels.PointStruct(
                id=d.id,
                vector=v,
                payload={"text": d.text},
            )
            for d, v in zip(docs, vectors)
        ],
    )


def search_similar(query: str, limit: int = 4) -> list[str]:
    """
    クエリに近いドキュメントの text を上位 limit 件返す。
    """
    client = get_qdrant_client()
    query_vector = embed_text(query)

    result = client.search(
        collection_name=_settings.qdrant_collection,
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
