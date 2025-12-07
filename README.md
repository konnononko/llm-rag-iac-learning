# llm-rag-iac-learning

[![CI](https://github.com/konnononko/llm-rag-iac-learning/actions/workflows/ci.yml/badge.svg)](https://github.com/konnononko/llm-rag-iac-learning/actions/workflows/ci.yml)

このリポジトリは、**クラウドネイティブな RAG（Retrieval-Augmented Generation）サービス** を  
短期間で試作しながら学習することを目的としたプロジェクトです。

以下の技術を一通り触れながら、  
「LLM + RAG + IaC」の基本概念と構築手順を理解することを狙います。

- **LLM API**（OpenAI など）を使った推論処理
- **RAG** による文書検索 + 文脈補完の基本フロー
- **ベクトルストア** を活用した検索（Chroma → Qdrant へ発展予定）
- **FastAPI** による Web API 実装
- **Docker** による開発環境構築
- **Terraform** を用いたクラウド環境の IaC 管理

目的はクラウドネイティブな構成の一部を「素早く触りながら理解すること」です。

## Stack (planned)

- Backend: Python + FastAPI
- RAG: LangChain + Chroma (local) / Qdrant（オプション）
- LLM: OpenAI API
- Local Infra: Docker / docker-compose
- IaC: Terraform
- Cloud: AWS（Lightsail または EC2 から開始予定）

## Project Structure

- `backend/`  : FastAPI + RAG 実装
- `infra/docker/`  : ローカル開発環境（Docker）
- `infra/terraform/`  : IaC - AWS リソース管理

## Getting Started

### Requirements

- Python 3.12+
- Docker (Qdrant の起動に使用)

### Setup

```bash
git clone https://github.com/konnononko/llm-rag-iac-learning.git
cd llm-rag-iac-learning/backend

uv sync

cp .env.example .env
# OPENAI_API_KEY などを設定

# Qdrant 起動
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Ingest sample documents
uv run python -m app.ingest
```

## Usage

### Run API Server

```bash
cd backend
uv run uvicorn app.main:app --reload
```

API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Health Check

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

### RAG Query Example

```bash
curl -X POST "http://localhost:8000/rag/query" -H "Content-Type: application/json" -d '{"query": "このプロジェクトの目的は？"}'
```
### Run Tests

```bash
cd backend
# linter check
uv run ruff check .
# run tests
uv run pytest
```

## Changelog

### v0.1.0 – RAG Pipeline Minimum Viable Version

- Qdrant + OpenAI embeddings + FastAPI
- CI pipeline (pytest / ruff / lint OK)
- FAQ-style RAG response working
