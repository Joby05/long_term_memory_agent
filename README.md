# Long-term Memory Chat Agent

This repository contains a small CLI-based long-term memory chat agent that extracts simple facts from user messages, stores them locally, and uses them to enrich prompts sent to an LLM.

## Quick setup

- Create and activate a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or .\.venv\Scripts\activate.bat for cmd.exe
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Provide your OpenAI API key either as an environment variable or in a `.env` file at the project root with the key `OPENAI_API_KEY`.

Example `.env`:

```
OPENAI_API_KEY=sk-...
```

## Running

- Start the interactive chat loop:

```bash
python main.py
```

- Run the scenario/demo script (replays a sequence of example messages):

```bash
python scenario_demo.py
```

Persistent memories are stored in `data/memories.json`.

## Project components & architecture

- `main.py` — CLI chat loop that reads user input, extracts memories, retrieves relevant memories, builds prompts, and calls the LLM.
- `scenario_demo.py` — scripted demo that exercises the agent with example conversations.
- `llm_client.py` — thin wrapper that builds prompts and calls the OpenAI API.
- `memory.py` — `MemoryStore` class and `extract_memories()` helper for extracting and persisting simple user facts.
- `data/memories.json` — local JSON file used as persistent storage for extracted facts.

Simple data flow:

User -> (extract_memories) -> MemoryStore -> (get_relevant) -> build_prompt -> llm_client -> LLM -> Response

ASCII diagram:

```
[User Input]
     |
     v
[extract_memories] -> saves to -> [data/memories.json]
     |
     v
[get_relevant] -> [build_prompt] -> [llm_client] -> [OpenAI LLM]
     |
     v
  [Agent Response]
```

## Design decisions & tradeoffs

- Persistence: a plain JSON file (`data/memories.json`) was chosen for simplicity and ease of inspection. Tradeoff: no fast similarity search or scaling for many entries.
- Extraction: rule-based regexes are used for extracting simple facts (name, job, diet, learning). Tradeoff: simple and explainable but brittle and limited compared to an NLP/NER approach.
- Synchronous LLM calls: the code uses blocking calls to the OpenAI client for simplicity. Tradeoff: easier to read and run in a CLI, but not optimal for concurrency or throughput.
- Prompt construction: memory facts are concatenated into a short context for the assistant. Tradeoff: straightforward but may not scale well with many memories or handle relevance weighting.

## What I'd improve with more time

- Replace JSON storage with a lightweight vector database (FAISS, Milvus, or an embedded DB) for scalable relevance/similarity search and better recall.
- Use an NLP pipeline or NER model for robust memory extraction (handle dates, entities, varied phrasing).
- Add config management and structured logging, plus retry/backoff for LLM calls and rate limiting.
- Introduce async support and background persistence to avoid blocking the CLI on long LLM responses.
- Add unit and integration tests to cover extraction, storage, and the LLM interface. Add CI for linting and tests.
- Improve prompts with dynamic context selection and a token budget to avoid overly long requests.

## Files of interest

- [main.py](main.py) — interactive CLI loop
- [scenario_demo.py](scenario_demo.py) — scripted demo
- [llm_client.py](llm_client.py) — LLM wrapper and prompt builder
- [memory.py](memory.py) — memory store and extraction

## Next steps you can ask me to do

- Add tests for `extract_memories()` and `MemoryStore`.
- Replace JSON persistence with a small vector store example.
- Improve extraction using a simple spaCy or transformer-based NER pipeline.

---
Created to document the long-term-memory-agent repository and provide guidance for running and extending the project.
