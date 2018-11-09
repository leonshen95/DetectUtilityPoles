from django.shortcuts import render
from .models import Users
from test_nov6 import models
from django.shortcuts import HttpResponse

# Create your views here.
def map(request):
    if request.method == "POST":
        location = request.POST.get("latitude", None)
        #longitude = request.POST.get("longitude", None)

        print(longitude, latitude)
        #models.Coordinates.objects.create(longitude=longitude, latitude=latitude)

    #return HttpResponse("hello world!")
    return render(request, "map.html", )

def index(request):
    return render(request, "index.html")

def add_user(request):
    user = Users.objects.create(username='fuyao2', password='111')
    print(user)
    return HttpResponse('done!')
def show_user(request):
    show = Users.objects.all()
    for u in show:
        print(u)
    return HttpResponse(show)