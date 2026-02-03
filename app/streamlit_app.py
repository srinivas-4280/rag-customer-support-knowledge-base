import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS

st.set_page_config(page_title="FAST RAG App", layout="wide")
st.title("⚡ Customer Support Knowledge Base (FAST RAG App)")

# 1. Load local embedding model (NO HF download)
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedder = load_embedder()

# 2. Embedding wrapper (MAKES IT CALLABLE)
class EmbeddingWrapper:
    def __call__(self, text):
        # when FAISS calls embedding_function(text)
        return embedder.encode([text], convert_to_numpy=True)[0]

    def embed_documents(self, texts):
        return embedder.encode(texts, convert_to_numpy=True)

    def embed_query(self, text):
        return embedder.encode([text], convert_to_numpy=True)[0]

embedding_fn = EmbeddingWrapper()

# 3. Load FAISS DB
@st.cache_resource
def load_faiss():
    return FAISS.load_local(
        "models/vector_store",
        embeddings=embedding_fn,
        allow_dangerous_deserialization=True
    )

vector_store = load_faiss()

# 4. UI Input
query = st.text_input("Ask a question from the documents:")

# 5. Search
if query:
    with st.spinner("Searching..."):
        results = vector_store.similarity_search(query, k=3)

    st.subheader("📌 Top Answers:")
    for i, res in enumerate(results, start=1):
        st.write(f"**{i}. {res.page_content}**")
