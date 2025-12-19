from rag.loader import load_and_split_pdf
from rag.vectorstore import create_vectorstore

PDF_PATH = "data/Moby_Dick.pdf"

if __name__ == "__main__":
    chunks = load_and_split_pdf(PDF_PATH)
    print(chunks)
    create_vectorstore(chunks)
    print("✅ PDF ingested into Qdrant")
