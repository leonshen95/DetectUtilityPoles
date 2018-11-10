import urllib.request
<<<<<<< HEAD
heading=0
num=0
a="38.06344466"
b="-84.52000672"
for i in range(1,7):
    urllib.request.urlretrieve("https://maps.googleapis.com/maps/api/streetview?size=640x640&location="+a+","+b+"&heading="+str(heading)+"&key=AIzaSyAgfIHLW-ZOWqtEMQE_aC42ZBHZ6YhU_Fo",str(i)+".jpg")
    heading=heading+60
=======
urllib.request.urlretrieve("https://maps.googleapis.com/maps/api/streetview?size=640x640&location=38.06344466%2C-84.52000672&heading=42.71109980359694&pitch=5&fov=80&key=")
>>>>>>> e681d1169ea5a713a6c6ee8f2ff97e0e5266de9f
