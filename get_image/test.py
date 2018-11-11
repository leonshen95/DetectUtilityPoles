import classify_image
import urllib.request
import subprocess

program="./classify_image.py"
heading=0
num=0
a="42.348546"
b="-71.106549"
for i in range(1,7):
    urllib.request.urlretrieve("https://maps.googleapis.com/maps/api/streetview?size=640x640&location="+a+","+b+"&heading="+str(heading)+"&key=",str(i)+".jpg")
    heading=heading+60

# for i in range(1,7):
#     subprocess.run([program,"--image_file",str(i)+".jpg"])
subprocess.run([program])



