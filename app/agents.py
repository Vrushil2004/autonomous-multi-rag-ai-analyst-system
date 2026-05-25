import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts import (
    ANALYZER_PROMPT,
    PLANNER_PROMPT,
    SUMMARIZER_PROMPT,
)

# =========================================================
# Environment Configuration
# =========================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please configure it inside the .env file."
    )

# =========================================================
# OpenAI Client Initialization
# =========================================================

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-4o-mini"

# =========================================================
# Generic LLM Caller
# =========================================================

def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
) -> str:
    """
    Generic reusable LLM caller.

    Args:
        system_prompt: Instruction prompt
        user_prompt: User/task prompt
        temperature: Controls randomness

    Returns:
        Generated LLM response
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response.choices[0].message.content.strip()


# =========================================================
# Planner Agent
# =========================================================

def planner_agent(query: str) -> List[str]:
    """
    Breaks complex user queries into
    smaller executable reasoning steps.

    Example:
    Query:
    'Analyze financial risks in this report'

    Output:
    [
        'Retrieve financial sections',
        'Identify financial trends',
        'Detect major risks',
        'Generate recommendations'
    ]
    """

    response = call_llm(
        system_prompt=PLANNER_PROMPT,
        user_prompt=query,
        temperature=0.1,
    )

    # Clean and normalize steps
    steps = [
        step.strip("- ").strip()
        for step in response.split("\n")
        if step.strip()
    ]

    return steps


# =========================================================
# Analyzer Agent
# =========================================================

def analyzer_agent(
    query: str,
    contexts: List[str],
) -> str:
    """
    Performs deep reasoning and analysis
    on retrieved document context.
    """

    combined_context = "\n\n".join(contexts)

    user_prompt = f"""
    USER QUERY:
    {query}

    RETRIEVED CONTEXT:
    {combined_context}
    """

    analysis = call_llm(
        system_prompt=ANALYZER_PROMPT,
        user_prompt=user_prompt,
        temperature=0.2,
    )

    return analysis


# =========================================================
# Summarizer Agent
# =========================================================

def summarizer_agent(
    query: str,
    analysis: str,
) -> str:
    """
    Converts raw analysis into
    structured business insights.
    """

    user_prompt = f"""
    USER QUERY:
    {query}

    ANALYSIS RESULT:
    {analysis}
    """

    summary = call_llm(
        system_prompt=SUMMARIZER_PROMPT,
        user_prompt=user_prompt,
        temperature=0.2,
    )

    return summary