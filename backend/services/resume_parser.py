import re
from pathlib import Path
SKILLS = ["python","java","c++","javascript","sql","mysql","mongodb","fastapi","flask","node.js","react","rest api","docker","git","llm","prompt engineering","rag","embeddings","semantic search","machine learning","deep learning","nlp","pytorch","tensorflow","pandas","scikit-learn","aws","postgresql","faiss","chromadb","streamlit"]
def extract_text(filename, content):
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        import fitz
        doc = fitz.open(stream=content, filetype="pdf")
        return "\n".join(p.get_text() for p in doc).strip()
    if ext == ".docx":
        import io
        from docx import Document
        return "\n".join(p.text for p in Document(io.BytesIO(content)).paragraphs).strip()
    if ext in {".txt",".md"}: return content.decode("utf-8", errors="ignore").strip()
    raise ValueError("Upload PDF, DOCX, TXT, or MD.")
def extract_skills(text):
    t = re.sub(r"\s+", " ", text.lower())
    return sorted(s for s in SKILLS if re.search(r"(?<![a-z0-9])"+re.escape(s)+r"(?![a-z0-9])", t))
