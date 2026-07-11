# Chatterbox 💬

A Django multi-mode chatbot — one chat window, many personalities. Pick a mode
and the bot responds accordingly:

- 🎬 **Movie & TV Quotes** — replies with a famous quote
- 🧠 **Random Facts** — detects your topic and serves up a fact
- 🍌 **Minionese Translator** — turns your message into Minion-speak
- 🐉 **High Valyrian** — Game-of-Thrones-flavored translation
- 🏴‍☠️ **Pirate Speak** — aye, matey
- 🟢 **Yoda-Speak** — reorder your words, it does
- 💭 **Sentiment Mirror** — reads your mood and mirrors it back (lightweight NLP)
- ❓ **Trivia Game** — asks questions and tracks your score

## How it works

Every mode is a function `f(text, session) -> str`, registered in a single
`MODES` dictionary in `chattea_app/bot.py`. The view looks up the active mode
(kept in the Django **session**), calls `generate_reply()`, and saves the reply
— so **adding a personality is one function plus one line in `MODES`**; nothing
else changes.

- **Translators** are rule-based: a small English→X vocabulary plus a light
  phonetic transform and a random sign-off. No ML, no external calls.
- **Sentiment Mirror** uses a tiny positive/negative word lexicon rather than a
  heavy NLP library, keeping the app fast and deploy-friendly.
- **Trivia** is the one stateful mode: it stores score and the current answer in
  the session (and is listed in `STATEFUL_MODES` so the view seeds an opening
  question when you switch in). Score resets when you clear the chat.
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
