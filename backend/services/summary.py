import os
from typing import Any

import requests

# Keep generation bounded so prompts stay fast/cheap.
MAX_POSTS = 20
MAX_POST_CHARS = 280

SYSTEM_PROMPT = (
    "You are a neutral summarizer.\n"
    "Task: Summarize what people are discussing in the posts below about one topic.\n"
    "Rules:\n"
    "- Only use information from the posts.\n"
    "- 2-4 sentences total.\n"
    "- Neutral tone.\n"
    "- No quotes longer than a few words.\n"
    "- If there is not enough relevant content, output exactly:\n"
    "Not enough on-topic posts to summarize."
)

NOT_ENOUGH_TEXT = "Not enough on-topic posts to summarize."


def _env_str(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value.strip() if value and value.strip() else default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _clean_post_text(post: dict[str, Any]) -> str:
    text = str(post.get("text") or "").strip()
    if not text:
        return ""
    return text[:MAX_POST_CHARS]


def build_prompt(topic: str, posts: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for i, post in enumerate(posts[:MAX_POSTS], start=1):
        text = _clean_post_text(post)
        if not text:
            continue
        platform = str(post.get("platform") or "unknown")
        lines.append(f"{i}. [{platform}] {text}")

    if not lines:
        return f"Topic: {topic}\n\nPosts:\n\nSummary:"

    posts_block = "\n".join(lines)
    return f"Topic: {topic}\n\nPosts:\n{posts_block}\n\nSummary:"


def summarize_topic(topic: str, posts: list[dict[str, Any]]) -> str | None:
    """
    Returns:
      - summary string on success
      - NOT_ENOUGH_TEXT when no usable posts
      - None if Ollama call fails
    """
    topic = (topic or "").strip()
    if not topic:
        return NOT_ENOUGH_TEXT

    usable = [p for p in posts if _clean_post_text(p)]
    if not usable:
        return NOT_ENOUGH_TEXT

    # Read env at call time so script and Docker route can differ safely.
    base_url = _env_str("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    model = _env_str("OLLAMA_MODEL", "llama3:8b")
    timeout = _env_int("OLLAMA_TIMEOUT", 30)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(topic, usable)},
        ],
        "stream": False,
        "options": {"temperature": 0.2},
    }

    try:
        response = requests.post(f"{base_url}/api/chat", json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        text = str((data.get("message") or {}).get("content") or "").strip()
        return text if text else None
    except Exception:
        return None