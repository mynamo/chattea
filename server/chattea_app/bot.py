"""
chattea bot — multi-mode responders.

Each mode is just a function `f(text) -> str`. To add a new personality, write a
function and add one entry to MODES. Everything here is self-contained (no
external APIs or downloads) so it deploys cleanly on Render's free tier.
"""

import random
import re

# ---------------------------------------------------------------------------
# Mode 1 — Random facts about a topic
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


def facts_reply(text):
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
# Mode 2 — Famous movie & TV quotes
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


def quotes_reply(text):
    quote, source = random.choice(QUOTES)
    return f'"{quote}" — {source}'


# ---------------------------------------------------------------------------
# Mode 3 — Minionese translator
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
    # light phonetic minion-ification
    return core.replace("th", "d").replace("v", "b") or w


def minionese_reply(text):
    words = text.split()
    if not words:
        return "Bello! " + random.choice(MINION_EXCLAIM)
    translated = " ".join(_minionify_word(w) for w in words)
    return f"{translated.capitalize()}. {random.choice(MINION_EXCLAIM)}"


# ---------------------------------------------------------------------------
# Mode 4 — Sentiment mirror (lightweight lexicon-based NLP)
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


def sentiment_reply(text):
    tokens = re.findall(r"[a-z']+", text.lower())
    pos = sum(t in POS_WORDS for t in tokens)
    neg = sum(t in NEG_WORDS for t in tokens)
    score = pos - neg

    if score > 0:
        mood, emoji = "positive", "😄"
        line = "You sound upbeat — love that energy! Keep it going."
    elif score < 0:
        mood, emoji = "negative", "🫂"
        line = "I'm sensing some heaviness. That's okay — want to talk it out?"
    else:
        mood, emoji = "neutral", "🙂"
        line = "Feeling pretty even-keeled from what I can tell."

    detail = f"(read: {pos} positive / {neg} negative cue{'s' if (pos + neg) != 1 else ''})"
    return f"{emoji} I'm reading that as **{mood}**. {line} {detail}"


# ---------------------------------------------------------------------------
# Registry — add a personality by adding one line here
# ---------------------------------------------------------------------------
MODES = {
    "quotes": {"label": "🎬 Movie & TV Quotes", "func": quotes_reply},
    "facts": {"label": "🧠 Random Facts", "func": facts_reply},
    "minionese": {"label": "🍌 Minionese Translator", "func": minionese_reply},
    "sentiment": {"label": "💭 Sentiment Mirror", "func": sentiment_reply},
}
DEFAULT_MODE = "quotes"


def mode_choices():
    """[(key, label), ...] for the template's <select>."""
    return [(k, v["label"]) for k, v in MODES.items()]


def generate_reply(mode, text):
    mode = mode if mode in MODES else DEFAULT_MODE
    try:
        return MODES[mode]["func"](text)
    except Exception:
        return "Oops — my circuits hiccuped. Try again?"
