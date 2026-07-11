"""
Chatterbox bot — multi-mode responders.

Each mode is a function `f(text, session) -> str`. Most modes ignore `session`;
stateful ones (like Trivia) use it to remember score across turns. To add a new
personality, write a function and add one entry to MODES. Everything here is
self-contained (no external APIs or downloads) so it deploys cleanly on Render.
"""

import random
import re


def _draw_from_deck(session, key, size):
    """Return the next index from a shuffled deck kept in the session, so items
    don't repeat until the whole set has been shown. Reshuffles when exhausted."""
    deck = session.get(key) or []
    if not deck:
        deck = list(range(size))
        random.shuffle(deck)
    i = deck.pop()
    session[key] = deck
    session.modified = True
    return i


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
    "sports": [
        "The Olympic gold medal is mostly silver — only about 6 grams of it is gold.",
        "A golf ball has, on average, 336 dimples.",
        "Basketball was invented using a peach basket in 1891.",
        "The fastest recorded tennis serve was over 163 mph.",
    ],
    "science": [
        "Bananas are slightly radioactive because they contain potassium-40.",
        "Hot water can freeze faster than cold water — the Mpemba effect.",
        "A teaspoon of a neutron star would weigh about six billion tons.",
        "Humans share about 60% of their DNA with bananas.",
    ],
    "movies": [
        "The 'Wilhelm scream' sound effect appears in hundreds of films.",
        "Toy Story was the first fully computer-animated feature film (1995).",
        "The Lord of the Rings trilogy used around 48,000 pieces of armor.",
        "Psycho was the first US film to show a toilet flushing on screen.",
    ],
    "geography": [
        "Russia spans 11 time zones.",
        "Africa is the only continent in all four hemispheres.",
        "Canada has more lakes than the rest of the world combined.",
        "The Sahara was green and full of lakes just ~6,000 years ago.",
    ],
    "health": [
        "Your body has more bacterial cells than human cells.",
        "The strongest muscle for its size is the masseter (jaw) muscle.",
        "You can't tickle yourself — your brain predicts the sensation.",
        "Laughing really does lower stress hormones.",
    ],
    "money": [
        "The '$' sign likely evolved from the Spanish peso abbreviation.",
        "More than 90% of the world's money exists only as digital records.",
        "The first credit card, the Diners Club (1950), was made of cardboard.",
        "Coins have ridged edges to stop people shaving off precious metal.",
    ],
}

# Common words that map to a topic (so 'tv'/'film' -> movies, 'planet' -> space, etc.)
_TOPIC_ALIASES = {
    "planet": "space", "star": "space", "galaxy": "space", "nasa": "space",
    "sea": "ocean", "fish": "ocean", "whale": "ocean",
    "animal": "animals", "dog": "animals", "cat": "animals", "pet": "animals",
    "war": "history", "ancient": "history", "king": "history",
    "eat": "food", "cooking": "food", "recipe": "food", "snack": "food",
    "tech": "technology", "computer": "technology", "ai": "technology", "phone": "technology",
    "song": "music", "band": "music", "guitar": "music",
    "sport": "sports", "soccer": "sports", "football": "sports", "basketball": "sports",
    "tv": "movies", "film": "movies", "movie": "movies", "show": "movies", "cinema": "movies",
    "country": "geography", "map": "geography", "world": "geography",
    "body": "health", "brain": "health", "medicine": "health",
    "cash": "money", "dollar": "money", "finance": "money", "currency": "money",
}
_FACT_INTRO = ["Here's a {topic} fact:", "Did you know? ({topic})", "Fun {topic} fact:",
               "🧠 {topic} corner:"]


def facts_intro(session=None):
    topics = ", ".join(FACTS.keys())
    return (f"🧠 Random Facts! I've got facts on: {topics}. "
            "Mention a topic and I'll pull one — or just say anything for a surprise fact.")


def facts_reply(text, session=None):
    low = text.lower()
    words = set(re.findall(r"[a-z]+", low))
    topic = next((t for t in FACTS if t in low or t[:-1] in low), None)
    if topic is None:  # try alias words like "tv" -> movies
        topic = next((_TOPIC_ALIASES[w] for w in words if w in _TOPIC_ALIASES), None)
    if topic is None:
        topic = random.choice(list(FACTS))
        prefix = "Not one of my topics, so here's a random one — "
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
    ("You talking to me?", "Taxi Driver"),
    ("Houston, we have a problem.", "Apollo 13"),
    ("Frankly, my dear, I don't give a damn.", "Gone with the Wind"),
    ("I see dead people.", "The Sixth Sense"),
    ("There's no place like home.", "The Wizard of Oz"),
    ("You shall not pass!", "The Lord of the Rings"),
    ("I'm the king of the world!", "Titanic"),
    ("Here's Johnny!", "The Shining"),
    ("Hasta la vista, baby.", "Terminator 2"),
    ("Nobody puts Baby in a corner.", "Dirty Dancing"),
    ("My precious.", "The Lord of the Rings"),
    ("I am your father.", "The Empire Strikes Back"),
    ("Keep your friends close, but your enemies closer.", "The Godfather Part II"),
    ("Wax on, wax off.", "The Karate Kid"),
    ("They may take our lives, but they'll never take our freedom!", "Braveheart"),
    ("You're gonna need a bigger boat.", "Jaws"),
    ("I feel the need — the need for speed.", "Top Gun"),
    ("Roads? Where we're going we don't need roads.", "Back to the Future"),
    ("Life finds a way.", "Jurassic Park"),
    ("This is Sparta!", "300"),
    ("Yippee-ki-yay.", "Die Hard"),
    ("I volunteer as tribute!", "The Hunger Games"),
    ("Bond. James Bond.", "Dr. No"),
    ("After all this time? Always.", "Harry Potter"),
    ("Legen — wait for it — dary.", "How I Met Your Mother"),
    ("Clear eyes, full hearts, can't lose.", "Friday Night Lights"),
    ("Treat yo self.", "Parks and Recreation"),
    ("The truth is out there.", "The X-Files"),
]


def quotes_reply(text, session=None):
    if session is None:
        quote, source = random.choice(QUOTES)
    else:
        i = _draw_from_deck(session, "quotes_deck", len(QUOTES))
        quote, source = QUOTES[i]
    return f'"{quote}" — {source}'


# ---------------------------------------------------------------------------
# Translator modes — they TRANSFORM what you type (they respond to your input)
# but don't leave the raw English words sitting in the reply.
# ---------------------------------------------------------------------------
def _words(text):
    return re.findall(r"[A-Za-z']+", text)


# --- Minionese: real translation where known, minion filler otherwise ---
MINION_VOCAB = {
    "hello": "bello", "hi": "bello", "hey": "bello", "goodbye": "poopaye", "bye": "poopaye",
    "thanks": "tank yu", "thank": "tank yu", "yes": "poka", "no": "noo",
    "i": "me", "you": "tu", "your": "tu", "my": "mi", "me": "me",
    "love": "tulaliloo", "friend": "bello", "friends": "bello", "food": "gelato",
    "hungry": "gelato", "eat": "gelato", "please": "para tu", "sorry": "bapple",
    "one": "hana", "two": "dul", "three": "sae",
}
MINION_FILLER = ["banana", "poopaye", "bello", "tulaliloo", "gelato", "poka", "bee do", "bapple"]
MINION_EXCLAIM = ["Banana!", "Poopaye!", "Tulaliloo ti amo!", "Bee do bee do!", "Poka poka!"]


def minionese_reply(text, session=None):
    words = _words(text)
    if not words:
        return "Bello! " + random.choice(MINION_EXCLAIM)
    out = [MINION_VOCAB.get(w.lower(), random.choice(MINION_FILLER)) for w in words]
    return " ".join(out).capitalize() + "! " + random.choice(MINION_EXCLAIM)


# --- High Valyrian: real words where known, Valyrian filler otherwise ---
VALYRIAN_VOCAB = {
    "hello": "rytsas", "hi": "rytsas", "hey": "rytsas", "goodbye": "geros ilas",
    "thanks": "kirimvose", "thank": "kirimvose", "yes": "kessa", "no": "daor",
    "i": "nyke", "me": "nyke", "you": "ao", "your": "aōha", "my": "ñuha",
    "love": "jorrāelan", "friend": "raqiros", "fire": "perzys", "dragon": "zaldrīzes",
    "king": "dārys", "queen": "dāria", "death": "morghon", "blood": "iksā", "is": "issa",
}
VALYRIAN_FILLER = ["valar", "morghulis", "dohaeris", "zaldrīzes", "perzys", "kirimvose",
                   "rytsas", "dārys", "iksā", "ñuha"]
VALYRIAN_SIGNOFF = ["Valar morghulis.", "Valar dohaeris.", "Dracarys!", "Kirimvose."]


def valyrian_reply(text, session=None):
    words = _words(text)
    if not words:
        return "Rytsas! " + random.choice(VALYRIAN_SIGNOFF)
    out = [VALYRIAN_VOCAB.get(w.lower(), random.choice(VALYRIAN_FILLER)) for w in words]
    return " ".join(out).capitalize() + ". " + random.choice(VALYRIAN_SIGNOFF)


# --- Pirate: an English dialect, so it reshapes your words (ye/be/arr, -in') ---
PIRATE_VOCAB = {
    "hello": "ahoy", "hi": "ahoy", "hey": "ahoy", "my": "me", "friend": "matey",
    "friends": "hearties", "you": "ye", "your": "yer", "are": "be", "is": "be",
    "am": "be", "was": "were", "yes": "aye", "no": "nay", "the": "th'", "for": "fer",
    "of": "o'", "to": "t'", "and": "an'", "money": "doubloons", "treasure": "booty",
    "food": "grub", "hungry": "starvin'", "drink": "grog", "water": "grog",
    "happy": "merry", "sad": "glum", "tired": "weary", "angry": "in a rage",
    "stop": "avast", "look": "spy", "help": "lend a hand", "captain": "cap'n",
    "ship": "vessel", "man": "scallywag", "woman": "lass", "boy": "lad", "girl": "lass",
    "yeah": "aye", "hello_there": "ahoy",
}
PIRATE_EXCLAIM = ["Arrr!", "Yo ho ho!", "Shiver me timbers!", "Avast ye!", "Yarrr, matey!"]


def pirate_reply(text, session=None):
    if not text.strip():
        return "Ahoy! " + random.choice(PIRATE_EXCLAIM)
    out = []
    for w in text.split():
        m = re.match(r"([A-Za-z']+)(\W*)$", w)
        if not m:
            out.append(w)
            continue
        core, tail = m.group(1), m.group(2)
        low = core.lower()
        if low in PIRATE_VOCAB:
            rep = PIRATE_VOCAB[low]
            out.append((rep.capitalize() if core[0].isupper() else rep) + tail)
        else:
            out.append(re.sub(r"ing\b", "in'", core) + tail)
    return " ".join(out) + " " + random.choice(PIRATE_EXCLAIM)


# --- Yoda: reorders your words (object-first) and adds a Yoda-ism ---
YODA_TAILS = ["Hmmm.", "Yes.", "Mmm, yes.", "Patience you must have.",
              "Strong with the Force, you are."]


def yoda_reply(text, session=None):
    clean = text.strip().rstrip(".!?")
    words = clean.split()
    if len(words) < 3:
        return (f"{clean.capitalize()}, yes. Hmmm." if clean else "Speak, you must. Hmmm.")
    split = max(1, len(words) * 2 // 3)
    sentence = " ".join(words[split:]) + ", " + " ".join(words[:split])
    sentence = sentence[0].upper() + sentence[1:]
    return sentence + ". " + random.choice(YODA_TAILS)


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
    ("What is the capital of Japan?", ["tokyo"]),
    ("How many strings does a standard guitar have?", ["6", "six"]),
    ("What is the powerhouse of the cell?", ["mitochondria", "mitochondrion"]),
    ("What planet is closest to the Sun?", ["mercury"]),
    ("In which country would you find the Eiffel Tower?", ["france"]),
    ("What is H2O more commonly known as?", ["water"]),
]


def _new_deck():
    deck = list(range(len(TRIVIA)))
    random.shuffle(deck)
    return deck


def _draw_question(session):
    """Pop the next question from a shuffled deck so none repeats until all are used."""
    deck = session.get("trivia_deck") or []
    if not deck:
        deck = _new_deck()
    i = deck.pop()
    session["trivia_deck"] = deck
    q, answers = TRIVIA[i]
    session["trivia_answer"] = answers
    session["trivia_q"] = q
    session.modified = True
    return q


def start_trivia(session):
    """Reset score/deck and return the intro + first question. Called on entering the mode."""
    session["trivia_score"] = 0
    session["trivia_total"] = 0
    session["trivia_deck"] = _new_deck()
    q = _draw_question(session)
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

    q = _draw_question(session)
    score = session["trivia_score"]
    total = session["trivia_total"]
    return f"{verdict}  (Score: {score}/{total})\n\nNext question: {q}"


# ---------------------------------------------------------------------------
# Registry — add a personality by adding one line here
# ---------------------------------------------------------------------------
MODES = {
    "quotes": {"label": "🎬 Movie & TV Quotes", "func": quotes_reply},
    "facts": {"label": "🧠 Random Facts", "func": facts_reply},
    "minionese": {"label": "🍌 Minionese", "func": minionese_reply},
    "valyrian": {"label": "🐉 High Valyrian", "func": valyrian_reply},
    "pirate": {"label": "🏴‍☠️ Pirate Speak", "func": pirate_reply},
    "yoda": {"label": "🟢 Yoda-Speak", "func": yoda_reply},
    "sentiment": {"label": "💭 Sentiment Mirror", "func": sentiment_reply},
    "trivia": {"label": "❓ Trivia Game", "func": trivia_reply},
}
DEFAULT_MODE = "quotes"
STATEFUL_MODES = {"trivia"}  # kept for the clear/reset logic in the view

# Modes that greet you with an opening bot message when you switch into them.
MODE_OPENERS = {"trivia": start_trivia, "facts": facts_intro}


def opener_for(mode, session):
    """Return an opening bot message for a mode (or None)."""
    fn = MODE_OPENERS.get(mode)
    return fn(session) if fn else None


def mode_choices():
    """[(key, label), ...] for the template's <select>."""
    return [(k, v["label"]) for k, v in MODES.items()]


def generate_reply(mode, text, session=None):
    mode = mode if mode in MODES else DEFAULT_MODE
    try:
        return MODES[mode]["func"](text, session)
    except Exception:
        return "Oops — my circuits hiccuped. Try again?"
