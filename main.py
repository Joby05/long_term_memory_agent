from memory import MemoryStore, extract_memories
from llm_client import build_prompt, call_llm

def chat_loop():
    """Main chat interaction loop."""
    store = MemoryStore()
    
    print("Long-term memory chat agent")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_msg = input("You: ")
        if user_msg.lower() == "exit":
            break
        
        # Step 1: Extract memories from message
        new_mems = extract_memories(user_msg)
        for key, value in new_mems:
            store.upsert_memory(key, value)
        
        # Step 2: Get relevant memories
        relevant = store.get_relevant(user_msg)
        
        # Step 3: Get LLM response
        prompt = build_prompt(user_msg, relevant)
        answer = call_llm(prompt)
        
        print(f"Agent: {answer}\n")

if __name__ == "__main__":
    chat_loop()
