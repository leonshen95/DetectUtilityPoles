import os
import urllib.request
import subprocess
import shutil
polelist=[]

def same(x):
  try:
    for i in range(len(x)):
      if (int(x[i+1][0])-int(x[i][0])==1):
        del x[i+1]
        os.remove(str(x[i+1])+".jpg")
  except IndexError:
    pass
  if ("1.jpg" in x) and ("6.jpg" in x):
    del x[-1]
    os.remove("6.jpg")

def read_result():
    global polelist
    with open ("/Users/liuknan/Documents/GitHub/DetectUtilityPoles/get_image/darknet/build/darknet/x64/result.txt") as f:
        text=f.read().split()
    print(text)
    try:
        if text[6]=="poles:":
            polelist.append(text[0][-6:-1])
            shutil.copyfile("","")
    except IndexError:
        pass
    print(polelist)
# program="classify_image.py"
# heading=0
# num=0
# a="42.350120"
# b="-71.106552"
# for i in range(1,7):
#     urllib.request.urlretrieve("https://maps.googleapis.com/maps/api/streetview?size=640x640&location="+a+","+b+"&heading="+str(heading)+"&fov=120&key=AIzaSyC0YHD07RkF_YDfS2pHTCLnu-VQlkAabH0",str(i)+".jpg")
#     heading=heading+60
#
# # for i in range(1,7):
# #     subprocess.run([program,"--image_file",str(i)+".jpg"])
# # subprocess.run(["python3",program])
# os.system("python3 classify_image.py")
read_result()


