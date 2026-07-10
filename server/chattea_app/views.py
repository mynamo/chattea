from django.shortcuts import render, redirect

from .models import Chats
from .forms import SubmitMessage
from . import bot


def index(request):
    """Chat view: pick a mode, send a message, get a bot reply.

    Uses the POST-redirect-GET pattern so refreshing the page doesn't resend
    the last message. The active mode is remembered in the session.
    """
    mode = request.session.get("mode", bot.DEFAULT_MODE)

    # Switch mode via ?mode=... (from the selector), then redirect.
    requested = request.GET.get("mode")
    if requested in bot.MODES:
        request.session["mode"] = requested
        return redirect("index")

    # Clear the conversation.
    if request.GET.get("clear") == "1":
        Chats.objects.all().delete()
        return redirect("index")

    if request.method == "POST":
        form = SubmitMessage(request.POST)
        if form.is_valid():
            text = form.cleaned_data["message"]
            Chats.objects.create(messages=text, sender="user", mode=mode)
            reply = bot.generate_reply(mode, text)
            Chats.objects.create(messages=reply, sender="bot", mode=mode)
        return redirect("index")

    context = {
        "chats": Chats.objects.all(),
        "form": SubmitMessage(),
        "modes": bot.mode_choices(),
        "current_mode": mode,
        "current_label": bot.MODES[mode]["label"],
    }
    return render(request, "chattea_home.html", context)
