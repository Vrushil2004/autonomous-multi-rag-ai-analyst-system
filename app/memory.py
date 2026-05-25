from typing import Any, Dict, List

# =========================================================
# In-Memory Conversation Store
# =========================================================

"""
Temporary in-memory storage for:
- user queries
- intermediate analysis
- final outputs

NOTE:
This is an MVP implementation.

Production systems should use:
- Redis
- PostgreSQL
- MongoDB
- Vector memory stores
"""

conversation_memory: List[Dict[str, Any]] = []


# =========================================================
# Add Memory Entry
# =========================================================

def add_memory(
    query: str,
    analysis: str,
    response: str,
) -> None:
    """
    Store conversation details in memory.
    """

    memory_entry = {
        "query": query,
        "analysis": analysis,
        "response": response,
    }

    conversation_memory.append(memory_entry)


# =========================================================
# Retrieve Memory
# =========================================================

def get_memory() -> List[Dict[str, Any]]:
    """
    Return complete conversation memory.
    """

    return conversation_memory


# =========================================================
# Clear Memory
# =========================================================

def clear_memory() -> None:
    """
    Reset stored memory.
    """

    conversation_memory.clear()