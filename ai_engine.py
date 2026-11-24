
import os


def generate_response(prompt, document_context=""):
    """
    Main AI response function.

    A generative AI provider will be connected here
    once an eligible provider is selected.
    """

    if not prompt or not prompt.strip():
        return "Please enter a question."

    prompt = prompt.strip()

    if document_context:
        return (
            "Your question has been received.\n\n"
            "Relevant document information:\n"
            f"{document_context[:4000]}\n\n"
            "The generative AI provider has not yet been connected, "
            "so I cannot generate an AI answer from this information."
        )

    return (
        "Welcome to RRR AI Assistant!\n\n"
        "Your chatbot interface is ready, but a generative AI "
        "provider has not yet been connected.\n\n"
        "Please configure an eligible AI provider to enable "
        "general AI conversations."
    )
  
