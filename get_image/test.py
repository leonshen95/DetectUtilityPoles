import classify_image
import urllib.request
import subprocess
def runprogram(program, args, inputstr):
    coll_run = subprocess.run(
        [program, *args],
        input=inputstr.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)
program="./classify_image.py"
heading=0
num=0
a="42.379653"
b="-71.124635"
for i in range(1,7):
    urllib.request.urlretrieve("https://maps.googleapis.com/maps/api/streetview?size=640x640&location="+a+","+b+"&heading="+str(heading)+"&key=AIzaSyAgfIHLW-ZOWqtEMQE_aC42ZBHZ6YhU_Fo",str(i)+".jpg")
    heading=heading+60

for i in range(1,7):
    subprocess.run([program,"--image_file",str(i)+".jpg"])



