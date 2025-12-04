# llm-rag-iac-learning

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
