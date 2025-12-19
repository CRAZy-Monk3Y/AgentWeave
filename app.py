import streamlit as st
from graph.graph import build_graph

st.set_page_config(page_title="AI Weather + RAG Agent")
st.title("AI Weather & PDF Assistant")

graph = build_graph()

query = st.chat_input("Ask me something...")
if query:
    st.chat_message("user").write(query)

    result = graph.invoke({
        "question": query
    })

    st.chat_message("assistant").write(result["answer"])

    # 🔍 Show RAG details only if present
    if "chunks" in result:
        with st.expander("🔍 Retrieved Chunks (RAG Context)"):
            for i, chunk in enumerate(result["chunks"], start=1):
                st.markdown(f"**Chunk {i}:**")
                st.write(chunk)

    if "sources" in result:
        with st.expander("📄 Sources"):
            for src in result["sources"]:
                st.write(src)
