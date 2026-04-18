import json
import os
from typing import Any, Iterator

import requests
import streamlit as st
from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_HOST = os.getenv("PINECONE_INDEX_HOST")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "__default__")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "chat_history.json")
SEARCH_QUERY_LIMIT = max(1, int(os.getenv("SEARCH_QUERY_LIMIT", "2")))
RETRIEVE_TOP_K_PER_QUERY = max(1, int(os.getenv("RETRIEVE_TOP_K_PER_QUERY", "10")))

ALLOWED_KEYWORDS = (
    "roboracer",
    "f1tenth",
    "f1-tenth",
    "autonomous racing",
    "coursekit",
    "ese6150",
)


def validate_env() -> None:
    missing = [
        name
        for name, value in (
            ("OPENROUTER_API_KEY", OPENROUTER_API_KEY),
            ("PINECONE_API_KEY", PINECONE_API_KEY),
            ("PINECONE_INDEX_HOST", PINECONE_INDEX_HOST),
        )
        if not value
    ]
    if missing:
        st.error(f"Missing environment variables in demo/.env: {', '.join(missing)}")
        st.stop()


def load_local_history() -> list[dict[str, str]]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            data = json.load(f)
        if isinstance(data, list):
            cleaned = []
            for item in data:
                role = item.get("role")
                content = item.get("content")
                if role in {"user", "assistant"} and isinstance(content, str):
                    cleaned.append({"role": role, "content": content})
            return cleaned
    except Exception:
        return []
    return []


def save_local_history(messages: list[dict[str, str]]) -> None:
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)


@st.cache_resource(show_spinner=False)
def pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc, pc.Index(host=PINECONE_INDEX_HOST)


def embed_query(pc: Pinecone, text: str) -> list[float]:
    resp = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[text],
        parameters={"input_type": "query", "truncate": "END"},
    )
    return resp.data[0]["values"]


def retrieve_context(question: str, top_k: int = 10) -> list[dict[str, Any]]:
    pc, index = pinecone_index()
    qvec = embed_query(pc, question)
    res = index.query(
        vector=qvec,
        top_k=top_k,
        namespace=PINECONE_NAMESPACE,
        include_metadata=True,
    )
    return [
        {
            "score": float(match.score),
            "url": (match.metadata or {}).get("url", ""),
            "text": (match.metadata or {}).get("text", ""),
            "source": (match.metadata or {}).get("source", ""),
        }
        for match in (res.matches or [])
    ]


def retrieve_for_queries(queries: list[str], top_k: int) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()
    for q in queries:
        hits = retrieve_context(q, top_k=top_k)
        for hit in hits:
            key = ((hit.get("url") or "").strip(), (hit.get("text") or "").strip())
            if not key[0] and not key[1]:
                continue
            if key in seen_keys:
                continue
            seen_keys.add(key)
            merged.append(hit)
    merged.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)
    return merged


def is_domain_question(question: str, hits: list[dict[str, Any]]) -> bool:
    q = question.lower()
    if any(keyword in q for keyword in ALLOWED_KEYWORDS):
        return True
    if not hits:
        return False
    domain_hits = [
        h
        for h in hits
        if ("roboracer" in (h.get("url") or "").lower())
        or ("f1tenth" in (h.get("url") or "").lower())
    ]
    if not domain_hits:
        return False
    top_score = max(float(h.get("score", 0.0)) for h in domain_hits)
    # Keep this permissive because Pinecone search already narrows by indexed corpus.
    return top_score >= 0.02


def build_context(hits: list[dict[str, Any]], max_items: int = 5) -> str:
    lines: list[str] = []
    for i, hit in enumerate(hits[:max_items], start=1):
        text = (hit.get("text") or "").strip().replace("\n", " ")
        if len(text) > 1200:
            text = text[:1200] + "..."
        lines.append(
            f"[{i}] score={hit['score']:.4f}\n"
            f"url={hit.get('url')}\n"
            f"source={hit.get('source')}\n"
            f"text={text}"
        )
    return "\n\n".join(lines)


def citation_block(hits: list[dict[str, Any]], max_urls: int = 5) -> str:
    seen: set[str] = set()
    urls: list[str] = []
    for hit in hits:
        url = (hit.get("url") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        urls.append(url)
        if len(urls) >= max_urls:
            break
    if not urls:
        return ""
    lines = ["\n\nSources:"]
    for i, url in enumerate(urls, start=1):
        lines.append(f"{i}. [{url}]({url})")
    return "\n".join(lines)


def stream_openrouter(messages: list[dict[str, str]]) -> Iterator[str]:
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers,
        stream=True,
        timeout=90,
    )
    if resp.status_code >= 400:
        error_body = resp.text
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {error_body}")
    for raw_line in resp.iter_lines(decode_unicode=True):
        if not raw_line:
            continue
        line = raw_line.strip()
        if not line.startswith("data:"):
            continue
        data_str = line[len("data:") :].strip()
        if data_str == "[DONE]":
            break
        try:
            payload = json.loads(data_str)
            choices = payload.get("choices") or []
            if not choices:
                continue
            delta = choices[0].get("delta") or {}
            token = delta.get("content")
            if token:
                yield token
        except Exception:
            continue


def call_openrouter_json(messages: list[dict[str, str]]) -> dict[str, Any]:
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=90,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text}")
    data = resp.json()
    raw = data["choices"][0]["message"]["content"]
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Planner response is not a JSON object.")
    return parsed


def plan_search_queries(messages: list[dict[str, str]], limit: int) -> list[str]:
    planner_prompt = (
        "You are a retrieval query planner for a RoboRacer/F1TENTH assistant.\n"
        "Return ONLY valid JSON object with key 'queries'.\n"
        f"Rules:\n- Max {limit} queries\n- Keep each query short and factual\n"
        "- Focus on terms likely present in docs\n"
        "- If one query is enough, return one\n"
        'Example: {"queries": ["apriltag usage in f1tenth", "apriltag localization roboracer"]}'
    )
    planner_messages = [{"role": "system", "content": planner_prompt}] + messages[-6:]
    parsed = call_openrouter_json(planner_messages)
    raw_queries = parsed.get("queries", [])
    if not isinstance(raw_queries, list):
        return []
    cleaned = []
    for q in raw_queries:
        if isinstance(q, str):
            q = q.strip()
            if q:
                cleaned.append(q)
    return cleaned[:limit]


def retrieval_fallback_answer(question: str, hits: list[dict[str, Any]]) -> str:
    if not hits:
        return (
            "OpenRouter is unavailable and I couldn't find strong Pinecone matches for that question. "
            "Please retry after fixing the OpenRouter key/limits."
        )
    snippets = []
    for hit in hits[:3]:
        text = (hit.get("text") or "").strip().replace("\n", " ")
        if len(text) > 300:
            text = text[:300] + "..."
        snippets.append(f"- {text}")
    return (
        "OpenRouter is unavailable right now, so here are top Pinecone snippets relevant to your question:\n\n"
        + "\n".join(snippets)
        + citation_block(hits)
    )


def main() -> None:
    st.set_page_config(page_title="RoboRacer/F1TENTH Chat Demo", page_icon="🏁")
    st.title("🏁 RoboRacer + F1TENTH Chat")
    st.caption("OpenRouter chat with Pinecone retrieval. Answers are limited to RoboRacer/F1TENTH.")
    validate_env()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Clear local history"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.session_state.messages = [
                {"role": "assistant", "content": "History cleared. Ask about RoboRacer/F1TENTH."}
            ]
            save_local_history(st.session_state.messages)
            st.rerun()
    with col2:
        st.caption(f"History file: `{os.path.basename(HISTORY_FILE)}`")

    if "messages" not in st.session_state:
        history = load_local_history()
        st.session_state.messages = history if history else [
            {"role": "assistant", "content": "Ask me anything about the RoboRacer and F1TENTH stack."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask about RoboRacer / F1TENTH")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    save_local_history(st.session_state.messages)
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Retrieving context..."):
                # Step 1: Let the model plan up to N JSON-formatted retrieval queries.
                planner_messages = [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
                try:
                    planned_queries = plan_search_queries(planner_messages, SEARCH_QUERY_LIMIT)
                    search_queries = planned_queries if planned_queries else [question]
                except Exception:
                    # Planner is optional; fallback to direct retrieval query.
                    search_queries = [question]

                # Step 2: Retrieve top-k per query and merge unique results.
                hits = retrieve_for_queries(search_queries, top_k=RETRIEVE_TOP_K_PER_QUERY)

            if not is_domain_question(question, hits):
                answer = (
                    "I can only answer questions about RoboRacer and the F1TENTH stack. "
                    "Please ask within that scope."
                )
                placeholder.markdown(answer)
            else:
                system_prompt = (
                    "You are a focused assistant for RoboRacer and F1TENTH. "
                    "Use retrieved Pinecone context first when relevant, but you may use your own model knowledge "
                    "to fill gaps when retrieval is insufficient. "
                    "If you use facts from retrieved context, include explicit markdown URL citations in the answer "
                    "(for example: [source](https://...)). "
                    "Do not answer topics outside RoboRacer/F1TENTH.\n\n"
                    f"Search queries used: {search_queries}\n\n"
                    "Retrieved context:\n"
                    f"{build_context(hits, max_items=10)}"
                )
                llm_messages = [{"role": "system", "content": system_prompt}] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
                streamed_chunks: list[str] = []
                for token in stream_openrouter(llm_messages):
                    streamed_chunks.append(token)
                    placeholder.markdown("".join(streamed_chunks) + "▌")
                answer = "".join(streamed_chunks).strip()
                if "http" not in answer.lower() and hits:
                    answer += citation_block(hits)
                placeholder.markdown(answer)
        except Exception as e:
            answer = retrieval_fallback_answer(question, hits if "hits" in locals() else [])
            answer += f"\n\n(Underlying error: {e})"
            placeholder.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_local_history(st.session_state.messages)


if __name__ == "__main__":
    main()
