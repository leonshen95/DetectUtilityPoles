from django.shortcuts import render
from .models import Users
import json
import urllib.request
from django.shortcuts import HttpResponse
import urllib.request
import shutil
import os

polelist = []
def run_detection():
    os.chdir("/Users/liuknan/Documents/Github/DetectUtilityPoles/googlemapapp/darknet/build/darknet/x64/")
    for i in range (1,7):

        os.system("./darknet detector test data/obj.data yolov3-tiny-obj.cfg backup/yolov3-tiny-obj_10000.weights /Users/liuknan/documents/github/DetectUtilityPoles/googlemapapp/static/streetviewimages/"+str(i)+".jpg -dont_show -ext_output < data/train.txt > /Users/liuknan/documents/github/DetectUtilityPoles/googlemapapp/static/result.txt")
        read_result()
def read_result():
    global polelist
    with open ("/Users/liuknan/documents/github/DetectUtilityPoles/googlemapapp/static/result.txt") as f:
        text=f.read().split()
    try:
        if text[6]=="poles:":
            polelist.append(text[0][-6:-1])
            shutil.copyfile("predictions.jpg","/Users/liuknan/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions/"+text[0][-6:-1])
    except IndexError:
        pass

def same(x):
  global polelist
  try:
    print(polelist)
    for i in range(len(x)):
      if (int(x[i+1][0])-int(x[i][0])==1):

        os.remove("/Users/liuknan/Documents/GitHub/DetectUtilityPoles/googlemapapp/static/predictions/"+str(x[i+1]))
        del x[i+1]
  except IndexError:
    pass
  if ("1.jpg" in x) and ("6.jpg" in x):

    os.remove("/Users/liuknan/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions/6.jpg")
    del x[-1]
  polelist=[]
  os.chdir("/Users/liuknan/Documents/Github/DetectUtilityPoles/googlemapapp")

# Create your views here.
def map(request):
    if request.method == "POST":
        latitude = request.POST.get("lat", None)
        longitude = request.POST.get("lng", None)


        #program = "D:/pyworkspace/DetectUtilityPoles/googlemapapp/test_nov6/classify_image.py"
        heading = 0
        for i in range(1, 7):
            urllib.request.urlretrieve(
                "https://maps.googleapis.com/maps/api/streetview?size=640x640&location=" + latitude + "," + longitude + "&heading=" + str(
                    heading) + "&fov=120&key=AIzaSyC0YHD07RkF_YDfS2pHTCLnu-VQlkAabH0", "./static/streetviewimages/"+ str(i) + ".jpg")
            heading = heading + 60
        shutil.rmtree("/Users/liuknan/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions")
        os.mkdir("/Users/liuknan/Documents/Github/DetectUtilityPoles/googlemapapp/static/predictions")
        run_detection()
        same(polelist)
        '''
        if os.path.exists('D:/pyworkspace/DetectUtilityPoles/googlemapapp/static/streetviewimages/polelist.txt'):

            f = open('D:/pyworkspace/DetectUtilityPoles/googlemapapp/static/streetviewimages/polelist.txt','r')
            for line in f.readlines():
                line = line.strip()
                polelist.append(line)
            f.close()

        print(polelist)
        '''
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


