# Chatterbox 💬

A Django multi-mode chatbot — one chat window, many personalities. Pick a mode
and the bot responds accordingly:

- 🎬 **Movie & TV Quotes** — replies with a famous quote
- 🧠 **Random Facts** — detects your topic and serves up a fact
- 🍌 **Minionese** — replies in Minion-speak
- 🐉 **High Valyrian** — replies with iconic Game-of-Thrones phrases
- 🏴‍☠️ **Pirate Speak** — talks like a pirate, aye
- 🟢 **Yoda-Speak** — speaks in Yoda-isms
- 💭 **Sentiment Mirror** — reads your mood and mirrors it back (lightweight NLP)
- ❓ **Trivia Game** — asks questions and tracks your score

## How it works

Every mode is a function `f(text, session) -> str`, registered in a single
`MODES` dictionary in `chattea_app/bot.py`. The view looks up the active mode
(kept in the Django **session**), calls `generate_reply()`, and saves the reply
— so **adding a personality is one function plus one line in `MODES`**; nothing
else changes.

- **Persona modes** (Minionese, Valyrian, Pirate, Yoda) reply with in-character
  lines from a curated set — they speak the voice rather than translating you.
- **Quotes & Facts** draw from curated sets using a shuffled "deck" kept in the
  session, so nothing repeats until the whole set has been shown.
- **Sentiment Mirror** uses a tiny positive/negative word lexicon rather than a
  heavy NLP library, keeping the app fast and deploy-friendly.
- **Trivia** is stateful: it stores score, the current answer, and its question
  deck in the session (and is in `STATEFUL_MODES` so the view seeds an opening
  question when you switch in).
- **A page refresh starts a fresh chat.** POST-redirect-GET preserves the
  conversation while you use it; a genuine reload clears it via a one-shot
  `keep_chat` session flag.
- Everything uses only the Python standard library (`random`, `re`), so
  `requirements.txt` stays minimal.

## Run locally

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/ — the home page redirects to the chat.

## Tech

Django · session-based mode selection · POST-redirect-GET · SQLite. Deployed on
Render (see `RENDER_DEPLOY.md`).
