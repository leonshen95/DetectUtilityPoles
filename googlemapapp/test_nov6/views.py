from django.shortcuts import render
from test_nov6 import models
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    if request.method == "POST":
        longitude = request.POST.get("longitude", None)
        latitude = request.POST.get("latitude", None)
        models.Coordinates.objects.create(longitude=longitude, latitude=latitude)
    latitude_list = 
    #return HttpResponse("hello world!")
    return render(request, "index.html",)