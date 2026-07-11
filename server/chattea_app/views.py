from django.shortcuts import render, redirect

from .models import Chats
from .forms import SubmitMessage
from . import bot

TRIVIA_KEYS = ("trivia_score", "trivia_total", "trivia_answer", "trivia_q", "trivia_deck")


def _reset_conversation(request):
    Chats.objects.all().delete()
    for k in TRIVIA_KEYS:
        request.session.pop(k, None)


def index(request):
    """Chat view: pick a mode, send a message, get a bot reply.

    Uses POST-redirect-GET so refreshing doesn't resend the last message. A
    genuine page load / refresh starts a fresh conversation — actions that
    should preserve the chat (sending a message, switching mode) set a one-shot
    `keep_chat` flag that the next GET consumes.
    """
    mode = request.session.get("mode", bot.DEFAULT_MODE)

    # Switch mode via ?mode=... (from the selector), then redirect.
    requested = request.GET.get("mode")
    if requested in bot.MODES:
        request.session["mode"] = requested
        # Some modes (Trivia, Facts) greet you with an opening bot message.
        opener = bot.opener_for(requested, request.session)
        if opener:
            Chats.objects.create(messages=opener, sender="bot", mode=requested)
        request.session["keep_chat"] = True
        return redirect("index")

    # Manual "Clear chat" link.
    if request.GET.get("clear") == "1":
        _reset_conversation(request)
        return redirect("index")

    if request.method == "POST":
        form = SubmitMessage(request.POST)
        if form.is_valid():
            text = form.cleaned_data["message"]
            Chats.objects.create(messages=text, sender="user", mode=mode)
            reply = bot.generate_reply(mode, text, request.session)
            Chats.objects.create(messages=reply, sender="bot", mode=mode)
        request.session["keep_chat"] = True
        return redirect("index")

    # Plain GET: if this isn't the post-redirect render, it's a fresh load /
    # refresh — so clear the conversation and start clean.
    if not request.session.pop("keep_chat", False):
        _reset_conversation(request)

    context = {
        "chats": Chats.objects.all(),
        "form": SubmitMessage(),
        "modes": bot.mode_choices(),
        "current_mode": mode,
        "current_label": bot.MODES[mode]["label"],
    }
    return render(request, "chattea_home.html", context)
