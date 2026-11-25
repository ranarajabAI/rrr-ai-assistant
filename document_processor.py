
def prepare_context(document_text, question, max_chars=12000):
    """
    Prepare document text for a future AI model.
    """

    if not document_text:
        return ""

    text = document_text[:max_chars]

    context = f"""
DOCUMENT CONTEXT:
{text}

USER QUESTION:
{question}

Use the document context to help answer the user's question.
If the context does not contain the answer, say so.
"""

    return context


def prepare_conversation(messages, max_messages=10):
    """
    Prepare recent conversation history.
    """

    return messages[-max_messages:]
