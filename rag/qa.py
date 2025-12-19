# rag/qa.py
from rag.vectorstore import load_vectorstore
from llm.model import get_llm

llm = get_llm()

def rag_answer(question: str):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an assistant that answers strictly using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    sources = [
        d.metadata.get("source", "PDF")
        for d in docs
    ]

    chunks = [
        d.page_content
        for d in docs
    ]

    return response.content, sources, chunks
