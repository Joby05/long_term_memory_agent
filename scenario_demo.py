from memory import MemoryStore, extract_memories
from llm_client import build_prompt, call_llm

def run_step(store, user_msg):
    """Process one user message and print response."""
    new_mems = extract_memories(user_msg)
    for key, value in new_mems:
        store.upsert_memory(key, value)
    
    relevant = store.get_relevant(user_msg)
    prompt = build_prompt(user_msg, relevant)
    answer = call_llm(prompt)
    
    print(f"You: {user_msg}")
    print(f"Agent: {answer}")
    print()

def demo_scenario():
    print("Long-term memory agent - scenario demo\n")
    
    # Conversation 1: Initial facts
    store = MemoryStore()
    conv1 = [
        "Hi! My name is Priya and I'm a software engineer at Stripe.",
        "I'm trying to learn Rust in my spare time.",
        "I'm vegetarian, by the way."
    ]
    print("=== Conversation 1 ===")
    for msg in conv1:
        run_step(store, msg)
    
    # Conversation 2: Lunch (new session)
    print("=== Conversation 2 (new session) ===")
    store = MemoryStore()
    run_step(store, "Can you recommend a good lunch spot near the office?")
    
    # Conversation 3: Job change
    print("=== Conversation 3 (new session) ===")
    store = MemoryStore()
    run_step(store, "I just switched jobs — I'm now at Figma!")
    
    # Conversation 4: What do you know about me
    print("=== Conversation 4 (new session) ===")
    store = MemoryStore()
    run_step(store, "What do you know about me?")
    
    # Conversation 5: Weekend project
    print("=== Conversation 5 (new session) ===")
    store = MemoryStore()
    run_step(store, "Suggest a weekend project for me.")
    
    print("Scenario complete.")
    print("Check data/memories.json for persistent storage.\n")

if __name__ == "__main__":
    demo_scenario()
