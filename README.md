# Chatterbox 💬

A Django multi-mode chatbot — one chat window, many personalities. Pick a mode
and the bot responds accordingly:

- 🎬 **Movie & TV Quotes** — replies with a famous quote
- 🧠 **Random Facts** — detects your topic and serves up a fact
- 🍌 **Minionese Translator** — turns your message into Minion-speak
- 💭 **Sentiment Mirror** — reads your mood and mirrors it back (lightweight NLP)

Adding a new personality is one function plus one line in `chattea_app/bot.py`.

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
