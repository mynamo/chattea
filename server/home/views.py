from django.shortcuts import redirect


def home(request):
    # Send visitors straight to the chat.
    return redirect("index")
