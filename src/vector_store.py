import os
import faiss
import numpy as np
import pickle
from typing import List, Any
from sentence_transformers import SentenceTransformer
from src.embedding import EmbeddingPipeline

class FaissVectorStore:
    
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.index = None
        self.metadata = []
        self.embedding_model = embedding_model
        self.model = SentenceTransformer(self.embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        print(f"[INFO] Loaded Embedding model: {self.embedding_model}")
        
    def build_from_documents(self, documents: List[Any]):
        print(f"Building Vector Store from {len(documents)} raw documents ...")
        emb_pipe = EmbeddingPipeline(model_name=self.embedding_model, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = emb_pipe.chunk_documents(documents)
        embeddings = emb_pipe.generate_embeddings(chunks)
        metadatas = [{"text": chunk.page_content} for chunk in chunks]
        self.add_embeddings(np.array(embeddings).astype('float32'), metadatas)
        self.save()
        print(f"[INFO] Vector Store built and saved to {self.persist_dir}")
        
    def add_embeddings(self, embeddings: np.ndarray, metadatas: List[Any] | None = None):
        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        if metadatas is not None:
            self.metadata.extend(metadatas)
        print(f"[INFO] Added {embeddings.shape[0]} embeddings to the vector store.")

    def save(self):
        faiss_path = os.path.join(self.persist_dir, "faiss.index")
        meta_path = os.path.join(self.persist_dir, "metadata.pkl")
        if self.index is None:
            raise ValueError("Cannot save: FAISS index is not initialized. Build or load first.")
        faiss.write_index(self.index, faiss_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"[INFO] Saved Faiss index and metadata to {self.persist_dir}")
        
    def load(self):
        faiss_path = os.path.join(self.persist_dir, "faiss.index")
        meta_path = os.path.join(self.persist_dir, "metadata.pkl")
        if os.path.exists(faiss_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(faiss_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            print(f"[INFO] Loaded Faiss index and metadata from {self.persist_dir}")
        else:
            print(f"[WARNING] No existing Faiss index or metadata found in {self.persist_dir}. Starting fresh.")
            
    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        if self.index is None:
            self.load()
        if self.index is None:
            raise ValueError("FAISS index is not initialized. Build or load before searching.")
        D, I = self.index.search(query_embedding.astype('float32'), top_k)
        results = []
        for idx, dist in zip(I[0],D[0]):
            if idx < 0:
                meta = None
            else:
                meta = self.metadata[idx] if idx < len(self.metadata) else None
            results.append({"index": idx, "distance": dist, "metadata": meta})
        return results
    
    def query(self, query_txt: str, top_k: int = 5):
        print(f"[INFO] Querying vector store for '{query_txt}'")
        query_emb = self.model.encode([query_txt]).astype('float32')
        return self.search(query_emb,top_k=top_k)
    