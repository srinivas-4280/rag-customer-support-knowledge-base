import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import numpy as np

print("🔄 Starting FREE RAG pipeline (FAST + OFFLINE)...")

# 1. Load PDFs
def load_documents():
    print("📄 Loading PDF files...")
    docs = []
    pdf_files = [
        "data/customer_FAQ.pdf",
        "data/Support_Tickets.pdf",
        "data/Troubleshooting_Guide.pdf"
    ]
    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        docs.extend(loader.load())
    print("✔ Loaded:", len(docs), "pages")
    return docs

# 2. Split into chunks
def split_documents(documents):
    print("✂️ Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40
    )
    chunks = splitter.split_documents(documents)
    print("✔ Total chunks:", len(chunks))
    return chunks

# 3. Create vector store
def create_vector_store(chunks):
    print("🧠 Loading offline fast embedding model...")
    
    # FAST + OFFLINE MODEL
    model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

    print("⚙️ Creating embeddings...")
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    print("📦 Building FAISS index...")
    text_embeddings = list(zip(texts, embeddings))

    vector_store = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=model
    )

    print("💾 Saving FAISS index...")
    vector_store.save_local("models/vector_store")

    print("✔ Vector DB saved successfully!")


# MAIN
if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    create_vector_store(chunks)
    print("🎉 FREE FAST RAG Pipeline Completed Successfully!")
