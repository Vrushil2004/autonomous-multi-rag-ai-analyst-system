import requests
import streamlit as st


# =========================================================
# Streamlit Page Configuration
# =========================================================

st.set_page_config(
    page_title="Autonomous AI Analyst System",
    page_icon="🧠",
    layout="wide",
)

st.title("Autonomous Multi-RAG AI Analyst System")

st.markdown(
    """
Enterprise-grade AI system for:
- Document Intelligence
- Semantic Retrieval
- Multi-Agent Analysis
- Context-Aware Question Answering
"""
)

BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# Upload Section
# =========================================================

st.subheader("Upload Enterprise Document")

uploaded_file = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"],
)

if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf",
        )
    }

    if st.button("Upload Document"):

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
        )

        if response.status_code == 200:

            st.success(
                "Document uploaded successfully"
            )

            st.json(response.json())

        else:

            st.error(
                "Document upload failed"
            )


# =========================================================
# Query Section
# =========================================================

st.subheader("Ask Questions")

query = st.text_area(
    "Enter analytical question",
    placeholder="Analyze major business risks from the uploaded document...",
)

if st.button("Generate AI Analysis"):

    payload = {
        "query": query
    }

    response = requests.post(
        f"{BASE_URL}/query",
        json=payload,
    )

    if response.status_code == 200:

        result = response.json()

        st.success(
            "Analysis generated successfully"
        )

        # -------------------------------------------------
        # Execution Plan
        # -------------------------------------------------

        if "execution_plan" in result:

            st.subheader("🛠 Execution Plan")

            st.write(
                result["execution_plan"]
            )

        # -------------------------------------------------
        # Agent Analysis
        # -------------------------------------------------

        if "analysis" in result:

            st.subheader("AI Analysis")

            st.write(
                result["analysis"]
            )

        # -------------------------------------------------
        # Final Response
        # -------------------------------------------------

        if "final_response" in result:

            st.subheader("Final Response")

            st.write(
                result["final_response"]
            )

    else:

        st.error(
            "Analysis generation failed"
        )