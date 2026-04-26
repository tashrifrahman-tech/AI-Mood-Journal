"""
ai.py — Google Gemini integration for AI Mood Journal.

Sends the user's journal entry to Gemini and parses back:
  - mood label      (e.g. "anxious", "content", "excited")
  - score           (1-10 float)
  - emotions list   (e.g. ["tired", "proud", "hopeful"])
  - summary         (2-sentence summary of the entry)
  - suggestion      (one actionable, empathetic tip)
  - color           (terminal color based on mood)

If GEMINI_API_KEY is not set, runs in DEMO MODE using
a rule-based fallback so the app still works for testing.
"""

import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-1.5-flash"   # free tier model


# ── Prompt ─────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a compassionate and insightful mood journal AI assistant.
Analyze the user's journal entry and respond ONLY with a valid JSON object.

Rules:
- Be empathetic, never judgmental
- Keep summary to 2 sentences max
- Suggestion must be ONE practical, kind, actionable tip
- Score is a float from 1.0 (worst) to 10.0 (best)
- Emotions list: 2 to 4 single words describing detected emotions
- Mood: single word from this list:
  ecstatic, happy, content, neutral, anxious, sad, angry,
  exhausted, hopeful, stressed, grateful, excited, lonely,
  motivated, overwhelmed
- Color: one of: bright_green, green, yellow, red, bright_red, cyan, magenta

Respond with ONLY this JSON structure, no markdown, no extra text:
{
  "mood": "content",
  "score": 6.5,
  "emotions": ["tired", "proud", "hopeful"],
  "summary": "You had a productive day despite feeling tired.",
  "suggestion": "Try a 10-minute walk to decompress before bed.",
  "color": "yellow"
}
"""


# ── Gemini API call ────────────────────────────────────────────────────────────

def analyze(journal_text: str) -> dict:
    """
    Send journal text to Gemini, return parsed mood analysis dict.
    Falls back to demo mode if no API key is set.
    """
    if not GEMINI_API_KEY:
        return _demo_analyze(journal_text)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        model    = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
        response = model.generate_content(journal_text)
        raw      = response.text.strip()

        # Strip markdown code fences if present
        raw = re.sub(r"```json|```", "", raw).strip()

        result = json.loads(raw)
        return _validate(result)

    except Exception as exc:
        return _demo_analyze(journal_text, error=str(exc))


# ── Validation ─────────────────────────────────────────────────────────────────

def _validate(result: dict) -> dict:
    """Ensure all required keys exist and values are in valid ranges."""
    valid_moods = {
        "ecstatic", "happy", "content", "neutral", "anxious",
        "sad", "angry", "exhausted", "hopeful", "stressed",
        "grateful", "excited", "lonely", "motivated", "overwhelmed",
    }
    valid_colors = {
        "bright_green", "green", "yellow", "red", "bright_red",
        "cyan", "magenta", "white",
    }

    mood  = result.get("mood", "neutral").lower()
    score = float(result.get("score", 5.0))

    return {
        "mood":       mood if mood in valid_moods else "neutral",
        "score":      max(1.0, min(10.0, score)),
        "emotions":   result.get("emotions", ["unknown"])[:4],
        "summary":    result.get("summary", "No summary available."),
        "suggestion": result.get("suggestion", "Take a moment to breathe and rest."),
        "color":      result.get("color", "yellow") if result.get("color") in valid_colors else "yellow",
    }


# ── Demo / Fallback mode ───────────────────────────────────────────────────────

def _demo_analyze(text: str, error: str = "") -> dict:
    """
    Rule-based fallback when Gemini API is unavailable.
    Uses simple keyword matching for a rough sentiment estimate.
    """
    text_lower = text.lower()

    positive = ["happy", "great", "amazing", "excited", "love", "wonderful",
                "fantastic", "good", "joy", "grateful", "proud", "accomplished",
                "motivated", "hopeful", "blessed", "productive"]
    negative = ["sad", "bad", "awful", "terrible", "hate", "angry", "stressed",
                "anxious", "worried", "depressed", "lonely", "upset", "frustrated",
                "exhausted", "tired", "overwhelmed", "hopeless", "failed"]
    neutral  = ["okay", "fine", "normal", "alright", "meh", "average"]

    pos = sum(1 for w in positive if w in text_lower)
    neg = sum(1 for w in negative if w in text_lower)

    if pos > neg + 1:
        mood, score, color = "happy",   7.5, "green"
        emotions = ["positive", "hopeful"]
    elif neg > pos + 1:
        mood, score, color = "stressed", 3.5, "red"
        emotions = ["stressed", "low"]
    else:
        mood, score, color = "neutral",  5.0, "yellow"
        emotions = ["neutral", "reflective"]

    note = ""
    if error:
        note = f" [API error: {error[:60]}]"

    return {
        "mood":       mood,
        "score":      score,
        "emotions":   emotions,
        "summary":    f"Your entry reflects a {mood} tone.{note} (Demo mode — add API key for full AI analysis)",
        "suggestion": "Take a moment to reflect on three things you are grateful for today.",
        "color":      color,
        "_demo":      True,
    }


def is_demo_mode() -> bool:
    return not bool(GEMINI_API_KEY)
