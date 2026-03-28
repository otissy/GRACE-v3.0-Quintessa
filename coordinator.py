import multiprocessing
import os
import sys
from agent_core import QuintessaBrain
from model_selector import select_model
from ingress import ear_loop
from egress import mouth_loop

def brainstorm_loop(ingress_q, egress_q, model_name):
    agent = QuintessaBrain(model_name)
    print(f"--- E.D.I.T.H. Brain Active ({model_name} Protocols) ---")
    
    while True:
        try:
            cmd, data = ingress_q.get(timeout=1)
            
            if cmd == "WAKE":
                # Kill speech if still talking
                egress_q.put(("KILL", ""))
                egress_q.put(("SPEAK", "Yeah? Listening."))
                continue

            elif cmd == "INPUT":
                # Brain processing (Logic Dispatch)
                ingress_text = data
                logic_out = agent.logic_dispatch(ingress_text)
                egress_q.put(("SPEAK", logic_out))

        except:
            continue

def main():
    selected_model = select_model()
    if not selected_model:
        return

    ingress_q = multiprocessing.Queue()
    egress_q = multiprocessing.Queue()

    # Process 1: The Ear
    p_ear = multiprocessing.Process(target=ear_loop, args=(ingress_q,))
    # Process 2: The Mouth
    p_mouth = multiprocessing.Process(target=mouth_loop, args=(egress_q,))
    # Process 3: The Brain (Run in main or own process)
    # Keeping it simple, Brain runs in main thread's loop for this demo
    
    p_ear.start()
    p_mouth.start()

    try:
        brainstorm_loop(ingress_q, egress_q, selected_model)
    except KeyboardInterrupt:
        p_ear.terminate()
        p_mouth.terminate()
        print("E.D.I.T.H. Protocol Offline.")

if __name__ == "__main__":
    main()
