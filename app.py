import streamlit as st
from main import initialize_rag, ask_question

st.set_page_config(
    page_title="Claude Exam Guide Assistant",
    page_icon="🤖"
)

st.title("🤖 Claude Exam Guide Assistant")

@st.cache_resource
def load_app():
    return initialize_rag()

embedding_model, collection = load_app()

question = st.chat_input(
    "Ask a question..."
)

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Thinking..."):
        answer = ask_question(
            question,
            embedding_model
        )

    with st.chat_message("assistant"):
        st.write(answer)