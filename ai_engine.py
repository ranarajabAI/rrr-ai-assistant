
def generate_response(prompt, context=""):
    """
    RRR AI Assistant AI engine.
    This is a placeholder until a hosted AI provider is connected.
    """

    if context:
        prompt = f"""
        Use the following context to answer the user.

        Context:
        {context}

        User question:
        {prompt}
        """

    return (
        "The AI engine is not connected yet. "
        "We need to configure a hosted AI provider to generate answers."
    )
