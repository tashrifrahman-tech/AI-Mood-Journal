"""
data.py — JSON-based storage for AI Mood Journal.

Storage structure (journal.json):
{
  "entries": {
    "2025-04-14": {
      "text": "Today was exhausting but rewarding...",
      "timestamp": "2025-04-14 21:30",
      "mood": "content",
      "score": 6.5,
      "emotions": ["tired", "proud", "hopeful"],
      "summary": "A productive but draining day...",
      "suggestion": "Consider getting to bed earlier tonight.",
      "color": "yellow"
    }
  },
  "streak": {
    "current": 3,
    "longest": 7,
    "last_entry": "2025-04-14"
  }
}
"""

import json
import os
from datetime import date, datetime, timedelta
from collections import Counter

DATA_FILE = "journal.json"

SCORE_COLOR = {
    (9, 10): "bright_green",
    (7,  8): "green",
    (5,  6): "yellow",
    (3,  4): "red",
    (1,  2): "bright_red",
}

MOOD_EMOJI = {
    "ecstatic":    "🤩",
    "happy":       "😊",
    "content":     "🙂",
    "neutral":     "😐",
    "anxious":     "😟",
    "sad":         "😢",
    "angry":       "😠",
    "exhausted":   "😩",
    "hopeful":     "🌟",
    "stressed":    "😰",
    "grateful":    "🙏",
    "excited":     "🎉",
    "lonely":      "😔",
    "motivated":   "💪",
    "overwhelmed": "😵",
}


# ── Load / Save ────────────────────────────────────────────────────────────────

def _default() -> dict:
    return {
        "entries": {},
        "streak": {"current": 0, "longest": 0, "last_entry": ""},
    }


def load() -> dict:
    if not os.path.exists(DATA_FILE):
        return _default()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        for key in _default():
            data.setdefault(key, _default()[key])
        return data
    except (json.JSONDecodeError, KeyError):
        return _default()


def save(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


# ── Entries ────────────────────────────────────────────────────────────────────

def has_entry_today() -> bool:
    return date.today().isoformat() in load()["entries"]


def get_entry(date_str: str) -> dict | None:
    return load()["entries"].get(date_str)


def get_all_entries() -> dict:
    return load()["entries"]


def get_recent_entries(n: int = 7) -> list:
    entries = load()["entries"]
    sorted_keys = sorted(entries.keys(), reverse=True)
    return [(k, entries[k]) for k in sorted_keys[:n]]


def save_entry(date_str, text, mood, score, emotions, summary, suggestion, color):
    data = load()
    data["entries"][date_str] = {
        "text":       text,
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood":       mood,
        "score":      score,
        "emotions":   emotions,
        "summary":    summary,
        "suggestion": suggestion,
        "color":      color,
    }
    _update_streak(data, date_str)
    save(data)


def delete_entry(date_str: str) -> bool:
    data = load()
    if date_str not in data["entries"]:
        return False
    del data["entries"][date_str]
    save(data)
    return True


# ── Streak ─────────────────────────────────────────────────────────────────────

def _update_streak(data: dict, date_str: str) -> None:
    streak  = data["streak"]
    last    = streak.get("last_entry", "")
    current = streak.get("current", 0)

    if last:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()
        today     = datetime.strptime(date_str, "%Y-%m-%d").date()
        diff      = (today - last_date).days
        if diff == 1:
            current += 1
        elif diff == 0:
            pass
        else:
            current = 1
    else:
        current = 1

    streak["current"]    = current
    streak["longest"]    = max(streak.get("longest", 0), current)
    streak["last_entry"] = date_str


def get_streak() -> dict:
    return load()["streak"]


# ── Stats ──────────────────────────────────────────────────────────────────────

def get_stats() -> dict:
    entries = load()["entries"]
    if not entries:
        return {}

    scores   = [e["score"] for e in entries.values() if "score" in e]
    moods    = [e["mood"]  for e in entries.values() if "mood"  in e]
    emotions = []
    for e in entries.values():
        emotions.extend(e.get("emotions", []))

    mood_counts    = Counter(moods)
    emotion_counts = Counter(emotions)
    top_mood       = mood_counts.most_common(1)[0] if mood_counts else ("—", 0)
    top_emotion    = emotion_counts.most_common(1)[0] if emotion_counts else ("—", 0)

    return {
        "total":        len(entries),
        "avg_score":    round(sum(scores) / len(scores), 1) if scores else 0,
        "highest":      max(scores) if scores else 0,
        "lowest":       min(scores) if scores else 0,
        "top_mood":     top_mood,
        "top_emotion":  top_emotion,
        "all_emotions": emotion_counts.most_common(5),
    }


def score_to_color(score: float) -> str:
    for (lo, hi), color in SCORE_COLOR.items():
        if lo <= round(score) <= hi:
            return color
    return "white"
