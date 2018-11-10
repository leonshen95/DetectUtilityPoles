from django.shortcuts import render
from .models import Users
import json
from test_nov6 import models
import urllib.request
from django.shortcuts import HttpResponse

# Create your views here.
def map(request):
    if request.method == "POST":
        latitude = request.POST.get("lat", None)
        longitude = request.POST.get("lng", None)

        print(longitude, latitude)
        heading = 0
        num = 0
        for i in range(1, 7):
            urllib.request.urlretrieve(
                "https://maps.googleapis.com/maps/api/streetview?size=640x640&location=" + latitude + "," + longitude + "&heading=" + str(
                    heading) + "&key=AIzaSyAgfIHLW-ZOWqtEMQE_aC42ZBHZ6YhU_Fo", "./streetviewimages/"+ str(i) + ".jpg")
            heading = heading + 60
    return render(request, "map.html", )

def sign_up(request):
    if request.method == "POST":
        list = []
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        repassword = request.POST.get("re-password", None)
        '''
        if len(username)<6 or len(username)>20:
            err = 'username should be 6-20 characters or numbers'
            list.append(err)
            return render(request, "sign-up.html", {'List': json.dumps(list)})
        '''

        Users.objects.create(username=username, password=password, email=email)
    return render(request, "sign-up.html")

def index(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        try:
            u = Users.objects.get(username=username)
            if password == u.password:
                return render(request, "map.html")
            else:
                list = ['wrong password']
                print(json.dumps(list))
                return render(request, "index.html",{'List': json.dumps(list)})
        except:
            return render(request, "index.html")
    else:
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


