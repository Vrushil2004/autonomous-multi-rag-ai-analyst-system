import re
from typing import List

# =========================================================
# Text Cleaning Utilities
# =========================================================

def clean_text(text: str) -> str:
    """
    Clean raw document text.

    Operations:
    - Remove extra spaces
    - Remove unnecessary line breaks
    - Normalize whitespace
    """

    # Remove multiple spaces/newlines/tabs
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# =========================================================
# Text Validation
# =========================================================

def validate_text(text: str) -> bool:
    """
    Validate whether text is usable.

    Returns:
        True if valid
        False otherwise
    """

    if not text:
        return False

    if len(text.strip()) == 0:
        return False

    return True


# =========================================================
# Deduplicate Retrieved Context
# =========================================================

def remove_duplicate_contexts(
    contexts: List[str],
) -> List[str]:
    """
    Remove duplicate retrieved chunks
    while preserving order.
    """

    unique_contexts = []
    seen = set()

    for context in contexts:

        cleaned_context = context.strip()

        if cleaned_context not in seen:
            unique_contexts.append(cleaned_context)
            seen.add(cleaned_context)

    return unique_contexts


# =========================================================
# Basic Text Truncation Utility
# =========================================================

def truncate_text(
    text: str,
    max_length: int = 3000,
) -> str:
    """
    Truncate long text to avoid
    excessively large prompts.
    """

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..." 