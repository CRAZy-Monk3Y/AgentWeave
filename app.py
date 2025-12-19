import streamlit as st
from dotenv import load_dotenv
from graph.graph import build_graph

load_dotenv()

st.set_page_config(page_title="AgentWeave", page_icon="🧵")
st.title("🧵 AgentWeave")

graph = build_graph()

with st.sidebar:
    st.header("🧵 AgentWeave")
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            if "chunks" in message:
                with st.expander("🔍 Retrieved Chunks"):
                    for i, chunk in enumerate(message["chunks"], start=1):
                        st.markdown(f"**Chunk {i}:**")
                        st.write(chunk)

            if "sources" in message:
                with st.expander("📄 Sources"):
                    for src in message["sources"]:
                        st.write(src)

prompt = st.chat_input("Ask me something...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("🤔 Thinking..."):
        result = graph.invoke({
            "question": prompt
        })

    assistant_message = {
        "role": "assistant",
        "content": result["answer"]
    }

    if "chunks" in result:
        assistant_message["chunks"] = result["chunks"]

    if "sources" in result:
        assistant_message["sources"] = result["sources"]

    st.session_state.messages.append(assistant_message)

    with st.chat_message("assistant"):
        st.markdown(result["answer"])

        if "chunks" in result:
            with st.expander("🔍 Retrieved Chunks"):
                for i, chunk in enumerate(result["chunks"], start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)

        if "sources" in result:
            with st.expander("📄 Sources"):
                for src in result["sources"]:
                    st.write(src)
