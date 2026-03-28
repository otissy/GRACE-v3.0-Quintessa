import os
import chromadb
from sentence_transformers import SentenceTransformer
from FlagEmbedding import FlagReranker

class HybridRAG:
    def __init__(self, db_path="./chroma_db"):
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        # Force CPU-only as requested for compatibility
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 
        self.collection = self.chroma_client.get_or_create_collection(name="grace_memory")
        
        # BGE-reranker (M3) locally downloaded
        local_reranker = r'c:\Users\31615\Desktop\GRACE\models\bge-reranker-v2-m3'
        if os.path.exists(local_reranker):
            self.reranker = FlagReranker(local_reranker, use_fp16=False)
        else:
            self.reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=False)

    def add_to_memory(self, text, metadata=None):
        embedding = self.embed_model.encode(text).tolist()
        doc_id = str(hash(text))
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else None
        )

    def retrieve(self, query, top_k=5):
        query_embedding = self.embed_model.encode(query).tolist()
        # Vector search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2 # Retrieve more for reranking
        )
        
        docs = results['documents'][0]
        if not docs:
            return []

        # Rerank
        pairs = [[query, doc] for doc in docs]
        scores = self.reranker.compute_score(pairs)
        
        # Sort docs by score
        ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in ranked_docs[:top_k]]

if __name__ == "__main__":
    rag = HybridRAG()
    rag.add_to_memory("Grace version 3.0 launched on 2026-03-28 with sandwich architecture.")
    print(f"Retrieving: {rag.retrieve('When was Grace 3.0 launched?')}")
