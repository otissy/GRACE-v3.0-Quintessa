# 🛠️ Grace v3.0: Quintessa Upgrade To-Do List

## Architecture & Personality
- [X] **Soul.md**: Define Quintessa's 23yo, empathetic persona.
- [X] **Sandwich Architecture**: Ingress -> Logic -> Egress.
- [X] **Model Selection**: Enum-based startup selection (Ollama).

## RAG & Memory (Local & CPU-Only)
- [X] **ChromaDB Integration**: Persistent vector storage.
- [X] **Sentence Transformers**: Hybrid retrieval with BGE-reranker.
- [X] **CPU-Only**: Force embeddings and reranker to CPU for compatibility.

## Information Grounding & Search
- [X] **DuckDuckGo Search**: Auto-grounding for queries (prepending 'Google ').
- [X] **WebBaseLoader**: Load pages from URLs in prompts.
- [X] **Clean Terminal**: Suppress non-essential logs.

## Multimodal Action (Pending)
- [ ] **Beeper SDK**: Send/receive messages logic.
- [ ] **Google Workspace**: Calendar & Email read/write tools.
- [ ] **Qwen3-TTS**: High-fidelity Quintessa voice (v0.4.2 Large).
- [ ] **Self-Improvement**: Turn-based reflection (every 4 turns).

## Polish & UI
- [ ] **Interactive Dashboard**: Modern Vite/React frontend.
- [ ] **Final Verification**: End-to-end flow test.
