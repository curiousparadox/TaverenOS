from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Dict


@dataclass
class Message:
    role: str
    content: str


def parse_export(data: str) -> List[Message]:
    """Parse raw text or JSON from a ChatGPT export."""
    data = data.strip()
    messages: List[Message] = []
    if not data:
        return messages
    # Try JSON first
    try:
        obj = json.loads(data)
        if isinstance(obj, dict) and "messages" in obj:
            for m in obj["messages"]:
                role = m.get("author", {}).get("role") or m.get("role")
                parts = m.get("content", {}).get("parts") if isinstance(m.get("content"), dict) else m.get("content")
                if isinstance(parts, list):
                    content = "\n".join(parts)
                else:
                    content = str(parts)
                if role and content:
                    messages.append(Message(role=role, content=content))
        elif isinstance(obj, list):
            for m in obj:
                role = m.get("role")
                content = m.get("content")
                if role and content:
                    messages.append(Message(role=role, content=str(content)))
        if messages:
            return messages
    except json.JSONDecodeError:
        pass

    # Fallback simple text parsing
    current_role: Optional[str] = None
    current_lines: List[str] = []
    for line in data.splitlines():
        if line.startswith("User:"):
            if current_role and current_lines:
                messages.append(Message(role=current_role, content="\n".join(current_lines).strip()))
            current_role = "user"
            current_lines = [line[len("User:"):].strip()]
        elif line.startswith("Assistant:"):
            if current_role and current_lines:
                messages.append(Message(role=current_role, content="\n".join(current_lines).strip()))
            current_role = "assistant"
            current_lines = [line[len("Assistant:"):].strip()]
        else:
            current_lines.append(line)
    if current_role and current_lines:
        messages.append(Message(role=current_role, content="\n".join(current_lines).strip()))
    return messages


EEV_KEYWORDS = {
    "pressure": ["pressure"],
    "grief": ["grief", "sad", "loss"],
    "recursion": ["recursion", "recursive"],
    "product-dev": ["product", "dev", "development"],
    "godform": ["godform", "deity", "god"],
}

WIKILINKS = {
    "EEV": "EEV",
    "pressure": "Pressure",
    "grief": "Grief",
    "recursion": "Recursion",
    "product": "Product-Development",
    "godform": "Godform",
}


def tag_text(text: str) -> List[str]:
    """Return a list of symbolic tags present in the given text."""
    tags: List[str] = []
    lowered = text.lower()
    for tag, keywords in EEV_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            tags.append(tag)
    return tags


def compute_tag_scores(messages: Iterable[Message]) -> Dict[str, float]:
    """Return a weight score for each tag found in the messages."""
    total_words = 0
    occurrences: Dict[str, int] = {t: 0 for t in EEV_KEYWORDS}
    for m in messages:
        words = re.findall(r"\w+", m.content)
        total_words += len(words)
        lowered = m.content.lower()
        for tag, keywords in EEV_KEYWORDS.items():
            for kw in keywords:
                occurrences[tag] += len(re.findall(rf"\b{re.escape(kw)}\b", lowered))

    scores: Dict[str, float] = {}
    if total_words:
        for tag, count in occurrences.items():
            if count:
                scores[tag] = (count / total_words) * 1000
    return scores


def wikilink(text: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        word = match.group(0)
        link = WIKILINKS.get(word.lower())
        if link:
            return f"[[{link}]]"
        return word

    pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in WIKILINKS) + r")\b", re.IGNORECASE)
    return pattern.sub(replacer, text)


def to_markdown(messages: Iterable[Message], output_dir: Path, thread_id: str) -> Path:
    """Write the given messages to an Obsidian markdown file."""
    messages = list(messages)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    title = f"ChatGPT Thread {thread_id}"

    tag_scores = compute_tag_scores(messages)
    tags = {"chatgpt", *tag_scores.keys()}

    all_text = [f"**{m.role.title()}:** {wikilink(m.content)}" for m in messages]
    symbolic_weight = round(sum(tag_scores.values()), 2)

    frontmatter = (
        "---\n"
        f"title: {title}\n"
        f"tags: [{', '.join(sorted(tags))}]\n"
        f"timestamp: {timestamp}\n"
        f"thread_id: {thread_id}\n"
        f"symbolic_weight: {symbolic_weight}\n"
        "---\n"
    )
    body = "\n\n".join(all_text) + "\n"
    output_path = output_dir / f"{thread_id}.md"
    output_path.write_text(frontmatter + "\n" + body)
    return output_path

