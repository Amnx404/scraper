# Demo Chat (OpenRouter + Pinecone)

Simple chat interface that:

- stacks chat messages in-session,
- keeps chat history per browser session,
- retrieves context from Pinecone,
- sends the conversation + retrieved context to OpenRouter for answers,
- only answers questions related to RoboRacer / F1TENTH,
- adds source citations when Pinecone context is used.

## 1) Setup

From project root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r demo/requirements.txt
```

## 2) Configure env

Create `demo/.env` from `demo/.env.example` and fill values:

- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL` (optional; default `openai/gpt-4o-mini`)
- `PINECONE_API_KEY`
- `PINECONE_INDEX_HOST`
- `PINECONE_NAMESPACE` (optional; default `__default__`)
- `SEARCH_QUERY_LIMIT` (optional; default `2`)
- `RETRIEVE_TOP_K_PER_QUERY` (optional; default `10`)

## 3) Run

```bash
streamlit run demo/app.py
```

## Notes

- Domain guard is strict: out-of-scope questions are rejected.
- The app first asks the model to emit JSON retrieval queries (max `SEARCH_QUERY_LIMIT`),
  then retrieves top `RETRIEVE_TOP_K_PER_QUERY` per query from Pinecone with dedupe.
- If your index namespace differs, set `PINECONE_NAMESPACE` accordingly.
