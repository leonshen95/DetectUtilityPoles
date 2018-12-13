from django.shortcuts import render
from .models import Users
from .models import Locations
import json
import urllib.request
from django.shortcuts import HttpResponse
import urllib.request
import shutil
import os
import datetime

polelist = []
def run_detection():
    polelist = []
    os.chdir("/Users/wangfuyao/Documents/Github/DetectUtilityPoles/googlemapapp/darknet/build/darknet/x64/")
    for i in range (1,7):

        os.system("./darknet detector test data/obj.data yolov3-tiny-obj.cfg backup/yolov3-tiny-obj_10000.weights /Users/wangfuyao/documents/github/DetectUtilityPoles/googlemapapp/static/streetviewimages/"+str(i)+".jpg -dont_show -ext_output < data/train.txt > /Users/wangfuyao/documents/github/DetectUtilityPoles/googlemapapp/static/result.txt")
        a = read_result()
        if a == None:
            pass
        else:
            polelist.append(a)
    return polelist

def read_result():
    global polelist
    polelist = []
    with open ("/Users/wangfuyao/documents/github/DetectUtilityPoles/googlemapapp/static/result.txt") as f:
        text=f.read().split()
    try:
        if text[6]=="poles:":
            polelist.append(text[0][-6:-1])
            shutil.copyfile("predictions.jpg","/Users/wangfuyao/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions/"+text[0][-6:-1])
            return text[0][-6:-1]
    except IndexError:
        pass

def same(x):
  try:
    print(x)
    for i in range(len(x)):
      if (int(x[i+1][0])-int(x[i][0])==1):
        os.remove("/Users/wangfuyao/Documents/GitHub/DetectUtilityPoles/googlemapapp/static/predictions/"+str(x[i+1]))
        del x[i+1]
  except IndexError:
    pass
  if ("1.jpg" in x) and ("6.jpg" in x):

    os.remove("/Users/wangfuyao/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions/6.jpg")
    del x[-1]
  os.chdir("/Users/wangfuyao/Documents/Github/DetectUtilityPoles/googlemapapp")

# Create your views here.
def map(request):
    if request.method == "POST":
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        latitude = request.POST.get("lat", None)
        longitude = request.POST.get("lng", None)
        heading = 0
        for i in range(1, 7):
            urllib.request.urlretrieve(
                "https://maps.googleapis.com/maps/api/streetview?size=640x640&location=" + latitude + "," + longitude + "&heading=" + str(
                    heading) + "&fov=120&key=AIzaSyC0YHD07RkF_YDfS2pHTCLnu-VQlkAabH0", "./static/streetviewimages/" + str(i) + ".jpg")
            heading = heading + 60
        shutil.rmtree("/Users/wangfuyao/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions")
        os.mkdir("/Users/wangfuyao/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions")
        polelist = run_detection()
        same(polelist)
        if len(polelist)!=0:
            Locations.objects.create(time=now_time, lat=latitude, lng=longitude)
        locations = Locations.objects.all().values('lat','lng')
        for l in locations:
            print(l)
    return render(request, "map.html", {'data': polelist})

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        repassword = request.POST.get("re-password", None)

        if len(username)<6 or len(username)>20:
            err = 'username should be between 6-20'
            return render(request, "sign-up.html", {'msg': err})
        else:
            if len(password)<6 or len(password)>20:
                err = 'password should be between 6-20'
                return render(request, "sign-up.html", {'msg': err})
            else:
                if password != repassword:
                    err = 'password input failed'
                    return render(request, "sign-up.html", {'msg': err})
                else:
                    suc = 'Successfully signed up!'
        Users.objects.create(username=username, password=password, email=email)
        return render(request, "index.html", {'msg': suc})
    return render(request, "sign-up.html")


def index(request):
    polelist = []
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        try:
            u = Users.objects.get(username=username)
            if password == u.password:
                return render(request, "map.html", {'data': polelist})
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


