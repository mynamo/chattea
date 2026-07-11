"""
Chatterbox bot — multi-mode responders.

Each mode is a function `f(text, session) -> str`. Most modes ignore `session`;
stateful ones (like Trivia) use it to remember score across turns. To add a new
personality, write a function and add one entry to MODES. Everything here is
self-contained (no external APIs or downloads) so it deploys cleanly on Render.
"""

import random
import re

# ---------------------------------------------------------------------------
# Mode — Random facts about a topic
# ---------------------------------------------------------------------------
FACTS = {
    "space": [
        "A day on Venus is longer than its year — it rotates slower than it orbits the Sun.",
        "Neutron stars are so dense that a sugar-cube-sized piece would weigh about a billion tons.",
        "There are more stars in the observable universe than grains of sand on all of Earth's beaches.",
        "Space is completely silent — there's no air for sound waves to travel through.",
    ],
    "ocean": [
        "We've explored less than 5% of Earth's oceans — more people have been to space than the deep sea.",
        "The blue whale's heart is so big a human could swim through its arteries.",
        "Octopuses have three hearts and blue blood.",
        "The longest mountain range on Earth is underwater — the mid-ocean ridge runs about 65,000 km.",
    ],
    "animals": [
        "A group of flamingos is called a 'flamboyance.'",
        "Wombats produce cube-shaped poop.",
        "Sea otters hold hands while sleeping so they don't drift apart.",
        "A shrimp's heart is located in its head.",
    ],
    "history": [
        "Oxford University is older than the Aztec Empire.",
        "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid.",
        "The Great Fire of London in 1666 reportedly killed only a handful of people.",
        "Napoleon was once attacked by a horde of bunnies during a rabbit hunt.",
    ],
    "food": [
        "Honey never spoils — edible honey has been found in 3,000-year-old Egyptian tombs.",
        "Bananas are berries, botanically, but strawberries are not.",
        "Carrots were originally purple; the orange ones were cultivated later.",
        "Pineapples take about two years to grow a single fruit.",
    ],
    "technology": [
        "The first computer 'bug' was an actual moth stuck in a relay in 1947.",
        "More than 90% of the world's currency exists only digitally.",
        "The first 1GB hard drive (1980) weighed over 500 pounds and cost $40,000.",
        "The '@' symbol was used in commerce for centuries before email adopted it.",
    ],
    "music": [
        "The most-covered song of all time is The Beatles' 'Yesterday.'",
        "Monaco's army is smaller than its orchestra.",
        "A 'jiffy' is an actual unit of time — and so is a 'moment' (90 seconds, medieval).",
        "Listening to music releases dopamine, the same reward chemical as food and love.",
    ],
}
_FACT_INTRO = ["Here's a {topic} fact:", "Did you know? ({topic})", "Fun {topic} fact:",
               "🧠 {topic} corner:"]


def facts_reply(text, session=None):
    low = text.lower()
    topic = next((t for t in FACTS if t in low or t[:-1] in low), None)
    if topic is None:
        topic = random.choice(list(FACTS))
        prefix = "I don't have that exact topic, so here's a random one — "
    else:
        prefix = ""
    intro = random.choice(_FACT_INTRO).format(topic=topic)
    return f"{prefix}{intro} {random.choice(FACTS[topic])}"


# ---------------------------------------------------------------------------
# Mode — Famous movie & TV quotes
# ---------------------------------------------------------------------------
QUOTES = [
    ("May the Force be with you.", "Star Wars"),
    ("Why so serious?", "The Dark Knight"),
    ("I'm gonna make him an offer he can't refuse.", "The Godfather"),
    ("Here's looking at you, kid.", "Casablanca"),
    ("Winter is coming.", "Game of Thrones"),
    ("I am the one who knocks!", "Breaking Bad"),
    ("How you doin'?", "Friends"),
    ("That's what she said.", "The Office"),
    ("Life is like a box of chocolates.", "Forrest Gump"),
    ("To infinity and beyond!", "Toy Story"),
    ("I'll be back.", "The Terminator"),
    ("Just keep swimming.", "Finding Nemo"),
    ("With great power comes great responsibility.", "Spider-Man"),
    ("Say hello to my little friend!", "Scarface"),
    ("You can't sit with us!", "Mean Girls"),
    ("Elementary, my dear Watson.", "Sherlock Holmes"),
]


def quotes_reply(text, session=None):
    quote, source = random.choice(QUOTES)
    return f'"{quote}" — {source}'


# ---------------------------------------------------------------------------
# Mode — Minionese translator
# ---------------------------------------------------------------------------
MINION_VOCAB = {
    "hello": "bello", "hi": "bello", "hey": "bello",
    "goodbye": "poopaye", "bye": "poopaye",
    "thanks": "tank yu", "thank": "tank yu",
    "yes": "poka", "no": "noo",
    "i": "me", "you": "tu", "your": "tu", "my": "mi",
    "love": "tulaliloo", "friend": "bello", "friends": "bello",
    "food": "gelato", "hungry": "gelato", "eat": "gelato",
    "ice": "gelato", "cream": "gelato",
    "one": "hana", "two": "dul", "three": "sae",
    "apple": "apple", "toy": "bee do", "fire": "bee do bee do",
    "please": "para tu", "sorry": "bapple",
}
MINION_EXCLAIM = ["Banana!", "Poopaye!", "Tulaliloo ti amo!", "Bee do bee do!",
                  "Bello!", "Tank yu!", "Poka poka!"]


def _minionify_word(w):
    core = re.sub(r"[^a-z]", "", w.lower())
    if core in MINION_VOCAB:
        return MINION_VOCAB[core]
    if len(core) > 3 and random.random() < 0.35:
        return "banana"
    return core.replace("th", "d").replace("v", "b") or w


def minionese_reply(text, session=None):
    words = text.split()
    if not words:
        return "Bello! " + random.choice(MINION_EXCLAIM)
    translated = " ".join(_minionify_word(w) for w in words)
    return f"{translated.capitalize()}. {random.choice(MINION_EXCLAIM)}"


# ---------------------------------------------------------------------------
# Mode — High Valyrian (Game of Thrones)
# ---------------------------------------------------------------------------
VALYRIAN_VOCAB = {
    "hello": "rytsas", "hi": "rytsas", "hey": "rytsas",
    "goodbye": "geros ilas", "bye": "geros ilas",
    "thanks": "kirimvose", "thank": "kirimvose",
    "yes": "kessa", "no": "daor",
    "i": "nyke", "you": "ao", "your": "aōha", "my": "ñuha", "me": "nyke",
    "love": "jorrāelan", "friend": "raqiros", "friends": "raqirossa",
    "fire": "perzys", "dragon": "zaldrīzes", "dragons": "zaldrīzesse",
    "king": "dārys", "queen": "dāria", "man": "vala", "men": "valar",
    "woman": "riña", "death": "morghon", "die": "morghūlis",
    "serve": "dohaeras", "burn": "dracarys", "blood": "iksā", "is": "issa",
    "good": "sȳz", "hello_world": "rytsas",
}
VALYRIAN_SIGNOFF = ["Valar morghulis.", "Valar dohaeris.", "Dracarys!",
                    "Kirimvose.", "Ñuha raqiros.", "Perzys ānnkos jemās."]


def _valyrianify_word(w):
    core = re.sub(r"[^a-z]", "", w.lower())
    if core in VALYRIAN_VOCAB:
        return VALYRIAN_VOCAB[core]
    # light phonetic flavor for unknown words
    return core.replace("th", "z").replace("w", "v").replace("k", "kh") or w


def valyrian_reply(text, session=None):
    words = text.split()
    if not words:
        return "Rytsas! " + random.choice(VALYRIAN_SIGNOFF)
    translated = " ".join(_valyrianify_word(w) for w in words)
    return f"{translated.capitalize()}. {random.choice(VALYRIAN_SIGNOFF)}"


# ---------------------------------------------------------------------------
# Mode — Pirate speak
# ---------------------------------------------------------------------------
PIRATE_VOCAB = {
    "hello": "ahoy", "hi": "ahoy", "hey": "ahoy",
    "my": "me", "friend": "matey", "friends": "hearties",
    "you": "ye", "your": "yer", "you're": "ye be", "are": "be", "is": "be",
    "yes": "aye", "no": "nay", "the": "th'", "for": "fer", "of": "o'",
    "to": "t'", "and": "an'", "money": "doubloons", "treasure": "booty",
    "food": "grub", "drink": "grog", "stop": "avast", "man": "scallywag",
    "woman": "lass", "boy": "lad", "girl": "lass", "yeah": "aye",
    "hello_there": "ahoy",
}
PIRATE_EXCLAIM = ["Arrr!", "Yo ho ho!", "Shiver me timbers!", "Avast ye!",
                  "Yarrr, matey!", "Walk the plank!"]


def _piratify_word(w):
    m = re.match(r"([a-zA-Z']+)(\W*)$", w)
    if not m:
        return w
    core, tail = m.group(1), m.group(2)
    low = core.lower()
    if low in PIRATE_VOCAB:
        repl = PIRATE_VOCAB[low]
        if core[0].isupper():
            repl = repl.capitalize()
        return repl + tail
    core = re.sub(r"ing\b", "in'", core)  # runnin', sailin'
    return core + tail


def pirate_reply(text, session=None):
    if not text.strip():
        return "Ahoy! " + random.choice(PIRATE_EXCLAIM)
    translated = " ".join(_piratify_word(w) for w in text.split())
    return f"{translated} {random.choice(PIRATE_EXCLAIM)}"


# ---------------------------------------------------------------------------
# Mode — Yoda-speak
# ---------------------------------------------------------------------------
YODA_TAILS = ["Hmmm.", "Yes.", "Mmm, yes.", "Do or do not — there is no try.",
              "Strong with the Force, you are.", "Patience you must have."]


def yoda_reply(text, session=None):
    clean = text.strip().rstrip(".!?")
    if not clean:
        return "Speak, you must. Hmmm."
    words = clean.split()
    if len(words) < 3:
        return f"{clean.capitalize()}, yes. Hmmm."
    # Move the back half of the sentence to the front (object-first, Yoda style).
    split = max(1, len(words) * 2 // 3)
    front = " ".join(words[split:])
    back = " ".join(words[:split])
    sentence = f"{front}, {back}".strip()
    sentence = sentence[0].upper() + sentence[1:]
    return f"{sentence}. {random.choice(YODA_TAILS)}"


# ---------------------------------------------------------------------------
# Mode — Sentiment mirror (lightweight lexicon-based NLP)
# ---------------------------------------------------------------------------
POS_WORDS = {
    "good", "great", "awesome", "amazing", "love", "loved", "happy", "excited",
    "wonderful", "fantastic", "beautiful", "best", "joy", "glad", "yay", "nice",
    "cool", "fun", "win", "won", "hope", "grateful", "thrilled", "delighted",
}
NEG_WORDS = {
    "bad", "terrible", "awful", "sad", "hate", "hated", "angry", "upset", "tired",
    "worst", "cry", "crying", "hurt", "pain", "lonely", "anxious", "stressed",
    "annoyed", "frustrated", "sick", "fail", "failed", "lost", "worried", "ugh",
}


def sentiment_reply(text, session=None):
    tokens = re.findall(r"[a-z']+", text.lower())
    pos = sum(t in POS_WORDS for t in tokens)
    neg = sum(t in NEG_WORDS for t in tokens)
    score = pos - neg
    if score > 0:
        mood, emoji, line = "positive", "😄", "You sound upbeat — love that energy! Keep it going."
    elif score < 0:
        mood, emoji, line = "negative", "🫂", "I'm sensing some heaviness. That's okay — want to talk it out?"
    else:
        mood, emoji, line = "neutral", "🙂", "Feeling pretty even-keeled from what I can tell."
    detail = f"(read: {pos} positive / {neg} negative cue{'s' if (pos + neg) != 1 else ''})"
    return f"{emoji} I'm reading that as **{mood}**. {line} {detail}"


# ---------------------------------------------------------------------------
# Mode — Trivia game (stateful: score kept in the session)
# ---------------------------------------------------------------------------
TRIVIA = [
    ("What planet is known as the Red Planet?", ["mars"]),
    ("How many continents are there on Earth?", ["7", "seven"]),
    ("What is the largest mammal in the world?", ["blue whale", "whale"]),
    ("In what language is this app's bot written? (the programming one)", ["python"]),
    ("What gas do plants primarily absorb from the air?", ["carbon dioxide", "co2"]),
    ("Who wrote the play 'Romeo and Juliet'?", ["shakespeare"]),
    ("What is the chemical symbol for gold?", ["au"]),
    ("How many sides does a hexagon have?", ["6", "six"]),
    ("What is the tallest mountain above sea level?", ["everest", "mount everest"]),
    ("What year did the first human land on the Moon?", ["1969"]),
    ("What is the smallest prime number?", ["2", "two"]),
    ("Which ocean is the largest?", ["pacific"]),
]


def start_trivia(session):
    """Reset score and return the intro + first question. Called on entering the mode."""
    session["trivia_score"] = 0
    session["trivia_total"] = 0
    q, answers = random.choice(TRIVIA)
    session["trivia_answer"] = answers
    session["trivia_q"] = q
    session.modified = True
    return f"🎯 Trivia time! I'll ask, you answer. Question 1: {q}"


def trivia_reply(text, session):
    answers = session.get("trivia_answer")
    if not answers:  # safety — no active question
        return start_trivia(session)

    guess = text.strip().lower()
    if guess in ("score", "stop", "quit"):
        return (f"📊 Your score so far: {session.get('trivia_score', 0)} / "
                f"{session.get('trivia_total', 0)}. Keep going or switch modes anytime!")

    correct = any(a in guess for a in answers)
    session["trivia_total"] = session.get("trivia_total", 0) + 1
    if correct:
        session["trivia_score"] = session.get("trivia_score", 0) + 1
        verdict = "✅ Correct!"
    else:
        verdict = f"❌ Not quite — the answer was '{answers[0]}'."

    q, next_answers = random.choice(TRIVIA)
    session["trivia_answer"] = next_answers
    session["trivia_q"] = q
    session.modified = True

    score = session["trivia_score"]
    total = session["trivia_total"]
    return f"{verdict}  (Score: {score}/{total})\n\nNext question: {q}"


# ---------------------------------------------------------------------------
# Registry — add a personality by adding one line here
# ---------------------------------------------------------------------------
MODES = {
    "quotes": {"label": "🎬 Movie & TV Quotes", "func": quotes_reply},
    "facts": {"label": "🧠 Random Facts", "func": facts_reply},
    "minionese": {"label": "🍌 Minionese Translator", "func": minionese_reply},
    "valyrian": {"label": "🐉 High Valyrian", "func": valyrian_reply},
    "pirate": {"label": "🏴‍☠️ Pirate Speak", "func": pirate_reply},
    "yoda": {"label": "🟢 Yoda-Speak", "func": yoda_reply},
    "sentiment": {"label": "💭 Sentiment Mirror", "func": sentiment_reply},
    "trivia": {"label": "❓ Trivia Game", "func": trivia_reply},
}
DEFAULT_MODE = "quotes"
STATEFUL_MODES = {"trivia"}  # modes that seed a bot message when you switch into them


def mode_choices():
    """[(key, label), ...] for the template's <select>."""
    return [(k, v["label"]) for k, v in MODES.items()]


def generate_reply(mode, text, session=None):
    mode = mode if mode in MODES else DEFAULT_MODE
    try:
        return MODES[mode]["func"](text, session)
    except Exception:
        return "Oops — my circuits hiccuped. Try again?"
