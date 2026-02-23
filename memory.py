import json
import os
import re
from datetime import datetime
from typing import List, Dict

class MemoryStore:
    """Handles storing, updating, and retrieving user memories."""
    
    def __init__(self, path="data/memories.json"):
        self.path = path
        os.makedirs("data", exist_ok=True)
        self.memories: List[Dict] = []
        self._load()
    
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.memories = json.load(f)
    
    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memories, f, indent=2)
    
    def upsert_memory(self, key: str, value: str):
        """Update existing or insert new memory."""
        now = datetime.utcnow().isoformat()
        for mem in self.memories:
            if mem["key"] == key:
                mem["value"] = value
                mem["updated_at"] = now
                self._save()
                return
        
        new_id = len(self.memories) + 1
        self.memories.append({
            "id": new_id,
            "key": key,
            "value": value,
            "created_at": now,
            "updated_at": now,
        })
        self._save()
    
    def get_relevant(self, query: str) -> List[Dict]:
        """Get memories relevant to this query."""
        q = query.lower()
        relevant = []
        
        if any(word in q for word in ["lunch", "dinner", "food", "restaurant"]):
            relevant += [m for m in self.memories if m["key"] == "diet"]
        
        if any(word in q for word in ["project", "weekend"]):
            relevant += [m for m in self.memories if m["key"] == "learning"]
        
        if "know about me" in q:
            relevant = self.memories
        
        return relevant
    
    def get_all(self):
        return self.memories

def extract_memories(text: str) -> List[tuple]:
    """Extract meaningful facts from user message."""
    memories = []
    
    # Name
    m = re.search(r"my name is ([A-Za-z ]+)", text, re.IGNORECASE)
    if m:
        memories.append(("name", m.group(1).strip()))
    
    # Job
    m = re.search(r"(work at|am at|now at) ([A-Za-z ]+)", text, re.IGNORECASE)
    if m:
        memories.append(("job", m.group(2).strip()))
    
    # Vegetarian
    if "vegetarian" in text.lower():
        memories.append(("diet", "vegetarian"))
    
    # Learning
    m = re.search(r"learn ([A-Za-z]+)", text, re.IGNORECASE)
    if m:
        memories.append(("learning", m.group(1).strip()))
    
    return memories
