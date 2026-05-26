# 🧠 AI Mood Journal 

A **CLI-based AI-powered mood journal** built with Python.  
Write about your day, and Google Gemini AI analyses your mood, detects emotions, gives you a wellness score, and tracks your mental wellbeing over time — all from your terminal.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=flat-square&logo=google)
![Storage](https://img.shields.io/badge/Storage-JSON-yellow?style=flat-square)

---

## ✨ Features

| Feature | Details |
|---|---|
| **AI Mood Analysis** | Google Gemini reads your journal and detects mood, emotions, score, and gives a wellness tip |
| **Mood Score** | Each entry gets a score from 1.0 (worst) to 10.0 (best) with a color-coded progress bar |
| **Emotion Tags** | AI extracts 2–4 emotion keywords like `#anxious`, `#proud`, `#hopeful` |
| **Daily Suggestion** | One kind, actionable wellness tip tailored to your current mood |
| **Streak Tracker** | Tracks your journaling streak — current and all-time best |
| **Mood Timeline** | See your last 7 or 14 entries in a formatted table with mood, score, and emotions |
| **ASCII Mood Chart** | Bar chart and sparkline trend of your mood scores over time |
| **All-Time Stats** | Average score, highest/lowest days, most common mood, top emotions |
| **Multi-line Input** | Free-text journaling — press Enter twice or type END to finish |
| **Demo Mode** | Works without an API key using rule-based sentiment fallback |
| **Persistent Storage** | All entries saved locally to `journal.json` — private, no cloud |

---

## 📸 Preview

```
╭─────────────────────────────────────────────────────────╮
│           🧠  AI  MOOD  JOURNAL                         │
│    Powered by Google Gemini · Your private journal      │
╰─────────────────────────────────────────────────────────╯

  Today      Sunday, 26 April 2026
  Mood       🙂 CONTENT
  Score      ████████░░░░  6.5/10
  Tip        Try a 10-minute walk to decompress before bed.
  🔥 Streak  3 day(s)   🏆 Best: 7 day(s)

  [ 1 ]  ✍️  Journal        [ 2 ]  📈  History & Charts
```

---

## 🗂️ Project Structure

```
MoodJournal/
│
├── main.py          # Entry point — dashboard + main menu
├── journal.py       # Tab 1 — Write, read, and delete entries
├── history.py       # Tab 2 — Timeline, charts, and stats
│
├── ai.py            # Google Gemini API integration + demo fallback
├── data.py          # JSON storage, streak tracking, stats engine
├── utils.py         # Rich display helpers, inputs, score bars
│
├── requirements.txt # Python dependencies
├── .env.example     # Template — copy to .env and add your API key
├── .gitignore       # Prevents .env and journal.json from being pushed
└── journal.json     # Auto-created on first run — your private entries
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AI-Mood-Journal.git
cd AI-Mood-Journal
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key

**Get your FREE Gemini API key (2 minutes, no credit card):**
1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key

**Create your `.env` file:**

On **Windows (Command Prompt):**
```cmd
copy .env.example .env
notepad .env
```

On **Mac / Linux:**
```bash
cp .env.example .env
nano .env
```

Replace the placeholder with your key:
```
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

### 4. Run the App
```bash
python main.py
```

> **No API key?** The app runs in **Demo Mode** automatically — mood analysis uses a rule-based fallback. All features still work; just add your key later for real AI analysis.

---

## 🖥️ How to Use

### ✍️ Tab 1 — Journal

**Writing an entry:**
- Select `1` from the main menu
- Type your entry freely (multi-line supported)
- Press **Enter twice** or type `END` on a new line to finish
- AI analysis runs automatically and shows mood, score, emotions, and a wellness tip

**Reading a past entry:**
- Select `2` from the Journal menu
- Enter a date in `YYYY-MM-DD` format
- See your original writing alongside the AI analysis

**Deleting an entry:**
- Select `3` from the Journal menu
- Enter the date and confirm with `y`

---

### 📈 Tab 2 — History & Charts

| Option | What it Shows |
|---|---|
| Timeline (7 entries) | Last 7 days — mood, score bar, emotions, summary |
| Timeline (14 entries) | Last 14 days |
| Bar Chart (7 entries) | Vertical ASCII bar chart of mood scores |
| Bar Chart (14 entries) | Same for 14 days |
| All Entries | Complete list of every entry ever written |
| All-Time Stats | Averages, streaks, top moods, top emotions |

---

## 🤖 How the AI Works

When you submit a journal entry, the text is sent to **Google Gemini 1.5 Flash** (free tier) with a structured system prompt. Gemini returns a JSON response:

```json
{
  "mood":       "content",
  "score":      6.5,
  "emotions":   ["tired", "proud", "hopeful"],
  "summary":    "A productive but draining day with moments of pride.",
  "suggestion": "Try a 10-minute walk to decompress before bed.",
  "color":      "yellow"
}
```

The app validates and renders this as a color-coded analysis panel. If the API call fails or no key is set, it falls back to keyword-based sentiment detection automatically — the app never crashes.

**Supported mood labels:**
`ecstatic` · `happy` · `content` · `neutral` · `anxious` · `sad` · `angry` · `exhausted` · `hopeful` · `stressed` · `grateful` · `excited` · `lonely` · `motivated` · `overwhelmed`

---

## 💾 Data & Privacy

- All journal entries are stored in `journal.json` **locally on your machine**
- **Nothing is stored in the cloud** — only your entry text is sent to Gemini for analysis, and Gemini does not store it
- Your `.env` file (API key) is listed in `.gitignore` and will **never be pushed to GitHub**
- Your `journal.json` is also in `.gitignore` — your diary stays private
- To back up your data, simply copy `journal.json`

---

## ⚠️ Windows Users — Important Notes

**Use `copy` instead of `cp` on Windows:**
```cmd
copy .env.example .env
```

**If Rich markup appears as plain text** (e.g. `[bold cyan]text[/bold cyan]`):
```cmd
pip install rich --upgrade
```

**For the best experience**, use **Windows Terminal** (free on the Microsoft Store) instead of the old Command Prompt — it supports full color, emoji, and Unicode rendering.

---

## 🏗️ Code Architecture

| Module | Responsibility |
|---|---|
| `main.py` | App entry point, main menu loop, today's dashboard |
| `journal.py` | Write/read/delete entry UI and logic (Tab 1) |
| `history.py` | Timeline, ASCII charts, and stats UI (Tab 2) |
| `ai.py` | Gemini API call, JSON parsing, validation, demo fallback |
| `data.py` | All JSON file I/O, streak tracking logic, stats engine |
| `utils.py` | Rich display helpers, input prompts, score bars, date utilities |

**Key design decisions:**
- `ai.py` is fully isolated — swap Gemini for any other LLM by editing one file
- `data.py` has zero UI code — clean separation of concerns
- Demo mode is fully automatic — the app never crashes without an API key
- All AI responses are validated before use — bad API output cannot break the app

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| [rich](https://github.com/Textualize/rich) | ≥ 13.0.0 | Terminal formatting, tables, panels, color |
| [google-generativeai](https://pypi.org/project/google-generativeai/) | ≥ 0.5.0 | Official Gemini Python SDK |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | ≥ 1.0.0 | Loads API key from `.env` file |

---

## 🐍 Concepts Practiced

- **AI / LLM integration** — calling a real generative AI API and parsing structured JSON responses
- **Prompt engineering** — writing a system prompt that forces clean JSON output from an LLM
- **Environment variables** — safely managing API keys with `.env` and `python-dotenv`
- **JSON file I/O** — reading, writing, and evolving a structured local data store
- **Modular design** — splitting a project into clean, single-responsibility files
- **Graceful error handling** — automatic fallback when API is unavailable or returns bad data
- **Rich terminal UI** — panels, tables, color-coded text, ASCII sparklines and bar charts

---

## 🔮 Possible Future Improvements

- Export mood history to PDF or CSV
- Weekly summary digest
- Voice journaling using `speech_recognition`
- Mood predictions based on past patterns
- Encryption of `journal.json` for extra privacy
- Multiple user profiles

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙋 Author

Built as part of a Python + AI learning journey.  
If this helped you, consider giving it a ⭐ on GitHub!
