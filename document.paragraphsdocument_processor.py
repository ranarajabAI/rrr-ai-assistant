
import re
from io import BytesIO

from pypdf import PdfReader
from docx import Document


def extract_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT files."""

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            pages = []

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append(
                        f"Page {page_number}:\n{text}"
                    )

            return "\n\n".join(pages)

        elif filename.endswith(".docx"):
            document = Document(uploaded_file)

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n".join(paragraphs)

        elif filename.endswith(".txt"):
            content = uploaded_file.read()

            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return content.decode("latin-1")

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            return (
                "This is an image file. Text extraction from "
                "images requires an OCR or image-understanding service."
            )

        else:
            return "Unsupported file format."

    except Exception as error:
        return f"File processing error: {error}"


def make_paragraphs(text, chunk_size=1000):
    """Divide document text into manageable sections."""

    if not text or not text.strip():
        return []

    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    paragraphs = []

    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1

        if current_length + word_length > chunk_size:
            paragraphs.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

        current_chunk.append(word)
        current_length += word_length

    if current_chunk:
        paragraphs.append(" ".join(current_chunk))

    return paragraphs


def search_documents(question, documents, top_k=3):
    """Find document sections relevant to a question."""

    if not question or not documents:
        return []

    question_words = set(
        re.findall(r"\b\w+\b", question.lower())
    )

    stop_words = {
        "the", "is", "are", "was", "were",
        "what", "when", "where", "who", "why",
        "how", "can", "could", "would", "should",
        "a", "an", "and", "or", "of", "to",
        "in", "on", "for", "with", "about"
    }

    question_words -= stop_words

    if not question_words:
        return []

    scored_results = []

    for document in documents:
        if isinstance(document, dict):
            content = document.get("content", "")
        else:
            content = str(document)

        content_words = set(
            re.findall(r"\b\w+\b", content.lower())
        )

        score = len(question_words & content_words)

        if score > 0:
            scored_results.append((score, content))

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        content
        for score, content in scored_results[:top_k]
    ]


def prepare_document(uploaded_file):
    """Extract and organize an uploaded document."""

    text = extract_text(uploaded_file)

    if not text or not text.strip():
        return []

    chunks = make_paragraphs(text)

    return [
        {
            "filename": uploaded_file.name,
            "content": chunk
        }
        for chunk in chunks
    ]
