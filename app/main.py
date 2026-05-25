from pathlib import Path
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.agents import (
    analyzer_agent,
    planner_agent,
    summarizer_agent,
)
from app.memory import conversation_memory
from app.rag import (
    process_document,
    retrieve_context,
)

# =========================================================
# FastAPI Application Configuration
# =========================================================

app = FastAPI(
    title="Autonomous AI Analyst System",
    description="Multi-Agent AI System with RAG and Reasoning",
    version="1.0.0",
)

# =========================================================
# Constants & Paths
# =========================================================

RAW_DOCUMENTS_PATH = Path("data/raw_docs")
RAW_DOCUMENTS_PATH.mkdir(parents=True, exist_ok=True)

ALLOWED_FILE_TYPES = [".pdf"]


# =========================================================
# Request Models
# =========================================================

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    execution_plan: List[str]
    analysis: str
    final_response: str


# =========================================================
# Health Check Endpoint
# =========================================================

@app.get("/")
def root():
    """
    Basic health check endpoint.
    """

    return {
        "status": "success",
        "message": "Autonomous AI Analyst System is running"
    }


# =========================================================
# Document Upload Endpoint
# =========================================================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process enterprise documents.
    Supported:
    - PDF
    """

    file_extension = Path(file.filename).suffix.lower()

    # Validate file type
    if file_extension not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Only PDF files are allowed."
        )

    # Save uploaded file
    file_path = RAW_DOCUMENTS_PATH / file.filename

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file: {str(e)}"
        )

    # Process document into vector database
    try:
        process_document(str(file_path))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )

    return {
        "status": "success",
        "filename": file.filename,
        "message": "Document uploaded and indexed successfully"
    }


# =========================================================
# Main Query Endpoint
# =========================================================

@app.post("/query", response_model=QueryResponse)
def query_system(request: QueryRequest):
    """
    Main AI analysis pipeline.

    Flow:
    1. Planner agent creates execution steps
    2. RAG retrieves context for each step
    3. Analyzer agent performs reasoning
    4. Summarizer agent generates structured response
    """

    user_query = request.query.strip()

    if not user_query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:
        # -------------------------------------------------
        # Step 1: Generate execution plan
        # -------------------------------------------------

        execution_plan = planner_agent(user_query)

        # -------------------------------------------------
        # Step 2: Retrieve relevant context
        # -------------------------------------------------

        retrieved_contexts = []

        for step in execution_plan:
            context = retrieve_context(step)
            retrieved_contexts.append(context)

        # -------------------------------------------------
        # Step 3: Perform AI analysis
        # -------------------------------------------------

        analysis_result = analyzer_agent(
            query=user_query,
            contexts=retrieved_contexts
        )

        # -------------------------------------------------
        # Step 4: Store memory
        # -------------------------------------------------

        conversation_memory.append({
            "query": user_query,
            "analysis": analysis_result
        })

        # -------------------------------------------------
        # Step 5: Generate final structured response
        # -------------------------------------------------

        final_response = summarizer_agent(
            query=user_query,
            analysis=analysis_result
        )

        return QueryResponse(
            query=user_query,
            execution_plan=execution_plan,
            analysis=analysis_result,
            final_response=final_response
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )