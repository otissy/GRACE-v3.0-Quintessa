# 🦾 GRACE (Generalized Robotic Assistant Core Engine) - v3.0

**Grace**, powered by the **Quintessa** Persona (v23), is a sophisticated agentic voice assistant designed for high-fidelity grounding, local memory, and autonomous self-improvement.

## 🚀 Key Features

*   **Sandwich Architecture**: Ingress (Voice/Beeper/Discord) → Logic (Ollama/RAG/Search) → Egress (TTS/Actions).
*   **Quintessa Persona**: An empathetic, 23-year-old digital companion defined in `Soul.md`.
*   **Hybrid RAG + BGE-M3**: High-fidelity retrieval and re-ranking for stable local memory.
*   **Intelligent Grounding**: DuckDuckGo search integration with automated URL loading via LangChain.
*   **Self-Improvement**: Autonomous reflection loop every 4 conversation turns.
*   **Multimodal Middleware**: To-do list tracking and action dispatching.

## 🛠️ Tech Stack

*   **Logic**: Ollama (Locked to NVIDIA-Nemotron-3-Nano).
*   **RAG/Memory**: ChromaDB + Sentence-Transformers (BGE-M3).
*   **Search**: DuckDuckGo-Search + BeautifulSoup4.
*   **Core**: LangChain + Python 3.11+.

## 🏗️ Installation

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/USER/GRACE.git
    cd GRACE
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    Create a `.env` file with your tokens:
    ```
    BEEPER_ACCESS_TOKEN=your_token
    GOOGLE_API_KEY=your_key
    ```
4.  **Run Grace**:
    ```bash
    python agent_core.py
    ```

## 📜 Soul & Directives
Read [Soul.md](Soul.md) for the internal logic and character guidelines for Quintessa.
Check [ToDo.md](ToDo.md) for current development status.
