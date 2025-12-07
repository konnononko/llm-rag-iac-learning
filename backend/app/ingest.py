from __future__ import annotations

from pathlib import Path

from .vector_store import Document, ensure_collection, index_documents


def load_readme_chunks() -> list[Document]:
    source_file = "README.md"
    readme_path = Path(__file__).resolve().parents[2] / source_file
    content = readme_path.read_text(encoding="utf-8")

    # 超ざっくり：行ベース or 固定長でチャンクに分割
    # 本格的には token 数ベースで分割したくなる
    chunk_size = 400
    chunks: list[str] = []
    buf = ""

    for line in content.splitlines():
        if len(buf) + len(line) + 1 > chunk_size:
            chunks.append(buf)
            buf = ""
        buf += line + "\n"
    if buf.strip():
        chunks.append(buf)

    docs: list[Document] = []
    for i, chunk in enumerate(chunks):
        docs.append(Document(id=i, text=chunk, source=source_file))

    return docs


def ingest_readme() -> None:
    ensure_collection()
    docs = load_readme_chunks()
    index_documents(docs)


if __name__ == "__main__":
    ingest_readme()
