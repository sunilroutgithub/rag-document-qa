def load_vector_store_for_rag(save_path: str = "faiss_index"):
    from langchain_community.embeddings import FakeEmbeddings
    embeddings = FakeEmbeddings(size=384)
    return FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )