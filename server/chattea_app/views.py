from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Chats
from .forms import SubmitMessage

# Create your views here.
def index(request):
    chats = Chats.objects.all().values()
    tp = loader.get_template("chattea_home.html")
    
    
    
    if request.method == "POST":
        form = SubmitMessage(request.POST)
        msg = Chats(messages=request.POST["message"])
        print("request type ", request.method)
        print("request data ", request.POST["message"])
        msg.save()
        print(Chats.objects.all().values())
    else: 
        form = SubmitMessage()
    context = {
        "chats": chats,
        "form": form
    }

    
    return HttpResponse(tp.render(context, request))


# def getMessage(request):
#     form = SubmitMessage()
#     return render(request, "chattea_home.html", {'form':form})