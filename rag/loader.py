from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_pdf(pdf_path: str):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"{pdf_path} not found")

    loader = PyPDFLoader(str(path))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=70,
        separators=["\n\n", "\n", ".", "!", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    return chunks
