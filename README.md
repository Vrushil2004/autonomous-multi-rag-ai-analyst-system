# Autonomous AI Analyst System

## Overview

Autonomous AI Analyst System is a multi-agent AI application that combines:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Semantic Search
- Multi-Step Reasoning
- Enterprise Document Analysis

The system processes enterprise documents such as PDFs, retrieves relevant contextual information using FAISS vector search, and generates structured analytical insights using multiple AI agents.

---

# Key Features

- Multi-Agent AI Workflow
- RAG-based Document Question Answering
- Semantic Search using FAISS
- PDF Document Ingestion
- Structured Insight Generation
- FastAPI Backend
- Dockerized Deployment
- Modular Architecture

---

# Architecture

```text
User Query
    ↓
Planner Agent
    ↓
Retriever (RAG + FAISS)
    ↓
Analyzer Agent
    ↓
Memory Layer
    ↓
Summarizer Agent
    ↓
Structured Response
```

---

# Tech Stack

## Programming
- Python

## Backend
- FastAPI

## LLM / GenAI
- OpenAI GPT
- LangChain

## Vector Database
- FAISS

## Embeddings
- Sentence Transformers

## Deployment
- Docker

---

# Project Structure

```text
ai-analyst-system/
│
├── app/
│   ├── main.py
│   ├── agents.py
│   ├── rag.py
│   ├── memory.py
│   ├── prompts.py
│   ├── utils.py
│
├── data/
│   ├── raw_docs/
│   ├── processed/
│
├── notebooks/
│
├── requirements.txt
├── Dockerfile
├── README.md
├── .env
```

---

# Installation

## Clone Repository

```bash
git clone <your-github-repository>
cd ai-analyst-system
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\\Scripts\\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

Application runs on:

```text
http://127.0.0.1:8000
```

---

# API Endpoints

## Upload Document

```http
POST /upload
```

Uploads and processes enterprise PDF documents.

---

## Query System

```http
POST /query
```

Example Request:

```json
{
  "query": "Analyze the major financial risks in this report"
}
```

---

# Sample Workflow

```text
Upload PDF
    ↓
Document Chunking
    ↓
Embedding Generation
    ↓
FAISS Vector Storage
    ↓
User Query
    ↓
Semantic Retrieval
    ↓
AI Analysis
    ↓
Structured Insights
```

---

# Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Persistent Memory
- Multi-Document Reasoning
- Hallucination Detection
- Evaluation Metrics Dashboard
- Streaming Responses
- Authentication & Authorization

---

# Author

Vrushil Shah

MSc Data Science | AI/ML Enthusiast | ML Engineering & GenAI