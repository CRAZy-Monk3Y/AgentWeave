import time
import uuid
import requests
import traceback
import streamlit as st
from dotenv import load_dotenv
from graph.graph import build_graph
from rag.kb_registry import delete_kb, load_registry, add_kb

load_dotenv()

st.set_page_config(page_title="AgentWeave", page_icon="🧵")
st.title("🧵 AgentWeave")


if "knowledge_bases" not in st.session_state:
    registry = load_registry()
    st.session_state.knowledge_bases = registry["knowledge_bases"]

if "current_kb" not in st.session_state:
    st.session_state.current_kb = None
with st.sidebar:
    st.header("🧵 AgentWeave")
    st.caption("Agentic AI with Tools & RAG")

    if st.button("🆕 New Chat", key="new_chat_btn"):
        st.session_state.messages = []
        st.rerun()
    st.subheader("📚 Knowledge Bases")

    kb_options = {
        kb["collection_id"]: f'{kb["filename"]} ({kb["collection_id"]})'
        for kb in st.session_state.knowledge_bases
    }

    if kb_options:
        selected_kb = st.selectbox(
            "Select active knowledge base",
            options=list(kb_options.keys()),
            format_func=lambda x: kb_options[x],
            key="kb_selector"
        )

        st.session_state.current_kb = selected_kb
    else:
        st.info("No knowledge bases available.")
    if st.session_state.current_kb:
        if st.button("🗑️ Delete Selected KB", key="delete_kb_btn"):
            kb_id = st.session_state.current_kb

            resp = requests.delete(
                f"http://localhost:6431/collections/{kb_id}"
            )

            if resp.status_code in (200, 404):
                delete_kb(kb_id)
                st.session_state.knowledge_bases = load_registry()["knowledge_bases"]
                st.session_state.current_kb = None

                st.success(f"Knowledge base `{kb_id}` deleted.")
                st.rerun()
            else:
                st.error("Failed to delete collection from Qdrant.")

graph = build_graph()

st.subheader("📄 Upload Knowledge Base")

uploaded_file = st.file_uploader(
    "Upload a PDF to create a new knowledge base",
    type=["pdf"],
    key="kb_uploader"
)

ingest=st.button("Ingest this document",disabled=not uploaded_file)

if uploaded_file and ingest:
    kb_id = f"kb_{uuid.uuid4().hex}"

    st.session_state.current_kb = kb_id

    pdf_path = f"data/{kb_id}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("📚 Ingesting document..."):
        from rag.loader import load_and_split_pdf
        from rag.vectorstore import create_vectorstore

        chunks = load_and_split_pdf(pdf_path)
        create_vectorstore(
            chunks,
            collection_name=kb_id
        )

    add_kb(
        collection_id=kb_id,
        filename=uploaded_file.name
    )

    st.session_state.knowledge_bases = load_registry()["knowledge_bases"]
    st.success("Knowledge base created and ready!")
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            if "chunks" in msg:
                with st.expander("🔍 Retrieved Chunks"):
                    for i, chunk in enumerate(msg["chunks"], start=1):
                        st.markdown(f"**Chunk {i}:**")
                        st.write(chunk)

            if "sources" in msg:
                with st.expander("📄 Sources"):
                    for src in msg["sources"]:
                        st.write(src)


def stream_text(text: str, delay: float = 0.01):
    for ch in text:
        yield ch
        time.sleep(delay)

prompt = st.chat_input("Ask me something...", key="agentweave_chat_input")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("🤔 Thinking..."):
            result = graph.invoke({"question": prompt})
    except Exception as e:
        traceback.print_exc()
        st.exception(e)
        st.stop()

    answer = result.get("answer", "Sorry, I couldn't generate a response.")

    assistant_message = {"role": "assistant", "content": answer}

    if "chunks" in result:
        assistant_message["chunks"] = result["chunks"]

    if "sources" in result:
        assistant_message["sources"] = result["sources"]

    st.session_state.messages.append(assistant_message)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed = ""

        for ch in stream_text(answer):
            streamed += ch
            placeholder.markdown(streamed)

        if "chunks" in result:
            with st.expander("🔍 Retrieved Chunks"):
                for i, chunk in enumerate(result["chunks"], start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)

        if "sources" in result:
            with st.expander("📄 Sources"):
                for src in result["sources"]:
                    st.write(src)
