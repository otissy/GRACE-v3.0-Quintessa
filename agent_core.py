from langchain_ollama import ChatOllama
from model_selector import select_model
from rag_manager import HybridRAG
from search_manager import SearchManager
from todo_middleware import ToDoMiddleware
import logging
import warnings
import os
from dotenv import load_dotenv

load_dotenv() # Load tokens from .env

# Clean terminal config
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("datasets").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning)
# Suppress torch/cuda output if possible
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# Logic Layer: Define Quintessa's "Brain"
class QuintessaBrain:
    def __init__(self, model_name):
        self.llm = ChatOllama(model=model_name)
        self.rag = HybridRAG()
        self.search_mgr = SearchManager()
        self.todo = ToDoMiddleware()
        self.turn_count = 0
        self.history = []
        self.soul_path = "Soul.md"
        self.soul_context = self.load_soul()

    def load_soul(self):
        try:
            with open(self.soul_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "No soul found."

    def process_ingress(self, input_text):
        """Ingress layer: Handle raw input from Voice/Beeper/Discord."""
        # TODO: Handle Beeper/Vosk specific ingress if needed
        return f"User said: {input_text}"

    def logic_dispatch(self, processed_ingress):
        """Logic layer: Process input with Quintessa's Persona, Search, and RAG memory."""
        # 1. Detect URLs for direct page loading
        urls = self.search_mgr.extract_urls(processed_ingress)
        web_context = ""
        if urls:
            web_context = "\n".join(self.search_mgr.load_url(urls[0]))
        
        # 2. Decide if search is needed for grounding (Simplest: Search if not just small talk)
        search_context = ""
        if not web_context and len(processed_ingress.split()) > 4: # Simple heuristic
             search_results = self.search_mgr.search(processed_ingress)
             search_context = "\n".join(search_results)
             
        # 3. Retrieve relevant context from RAG
        retrieved_context = self.rag.retrieve(processed_ingress, top_k=3)
        rag_str = "\n".join(retrieved_context) if retrieved_context else "No prior memory."
        
        prompt = f\"\"\"Persona Context:\n{self.soul_context}\n\nRecent History:\n{self.history[-10:]}\n\nRetrieved Context (RAG):\n{rag_str}\n\nSearch Grounding:\n{search_context}\n\nDirect Web Load:\n{web_context}\n\nInput: {processed_ingress}\n\nResponse:\"\"\"
        
        response = self.llm.invoke(prompt)
        
        # Save this interaction to RAG memory
        self.rag.add_to_memory(f"User: {processed_ingress}\nGrace: {response.content}")
        
        self.history.append((processed_ingress, response.content))
        self.turn_count += 1
        
        # Self-improvement loop: Every 4 turns
        if self.turn_count % 4 == 0:
            self.reflect()
            
        return response.content

    def egress_action(self, logic_response):
        """Egress layer: Handle final action (Speech/Text/API)."""
        # TODO: TTS layer integration with Qwen3-TTS
        print(f"Egress: {logic_response}")
        return logic_response

    def reflect(self):
        """Autonomous reflection on recent turns."""
        print("Reflecting on recent turns for self-improvement...")
        # TODO: Use the logic layer to suggest soul/skill updates
        pass

# Flow implementation
def main():
    selected_model = select_model()
    if not selected_model:
        return
    
    agent = QuintessaBrain(selected_model)
    print("\nGrace is active.")
    
    while True:
        user_input = input("\nYou: ")
        ingress = agent.process_ingress(user_input)
        logic_out = agent.logic_dispatch(ingress)
        agent.egress_action(logic_out)

if __name__ == "__main__":
    main()
