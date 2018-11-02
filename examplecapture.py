__copyright__ = """

    Copyright 2018 Osama Alshaykh, nxtec Corporation

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

# !/usr/bin/python

import csv
import sys, getopt
import numpy as np
import requests
import urllib
# import urllib2
import os
import time
import math
import pprint
from polycircles import polycircles
import json

Radius = .5
MAXRADIUS = 25
storefilename = 50
StreetViewRadius = 50
Radius_Steps = 10
No_Angles = 0
DeltaAngle = 5
heading = 0
pitch = 5
pitch2 = 10
FOV__0 = 80
FOV_MAX = 130
FOV_Step = 10  # 120 is maximum fov by stree view
size = '2000x2000'  # free is smaller
storefilename = 'poleimage'
TopY = 100
BottomY = 2000 - TopY
TopX = 100
BottomX = 2000 - TopX
PoleTop = 200
PoleBottom = 2000 - PoleTop

key = 'AIzaSyC0YHD07RkF_YDfS2pHTCLnu-VQlkAabH0'  # put your key here


# This function creates Directories

def newCoord(lon, lat, radius, angle_d):
    angle = math.pi * angle_d / 360
    dx = radius * math.cos(angle)
    dy = radius * math.sin(angle)
    point = {}
    point['lat'] = lat + (180 / math.pi) * (dy / 6372797.6)  # Earth Radius
    point['lon'] = lon + (180 / math.pi) * (dx / 6372797.6) / math.cos(lon * math.pi / 180)  # Earth Radius

    return point


def findCirclePoints(lon, lat, radius, N):
    # generate points
    circlePoints = []
    for k in range(N):
        angle = math.pi * k / N
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        point = {}
        point['lat'] = lat + (180 / math.pi) * (dy / 6372797.6)  # Earth Radius
        point['lon'] = lon + (180 / math.pi) * (dx / 6372797.6) / math.cos(lon * math.pi / 180)  # Earth Radius
        # add to list
        circlePoints.append(point)

    return circlePoints


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return
    except OSError:
        print('Error: Creating directory. ' + directory)
        return


def angleFromCoordinate(long1, lat1, long2, lat2):
    dLon = (long2 - long1)

    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

    brng = math.atan2(y, x)

    brng = math.degrees(brng)
    brng = (brng + 180) % 360

    return brng


def getCameraPosition(size, lon, lat, heading, pitch, fov, key):
    data = {}
    data['size'] = size
    loc = str(lat) + ',' + str(lon)
    data['location'] = loc
    data['heading'] = heading
    data['pitch'] = pitch
    data['fov'] = fov
    data['radius'] = StreetViewRadius
    data['key'] = key
    url_metadata = 'https://maps.googleapis.com/maps/api/streetview/metadata?' + urllib.urlencode(data)
    url = 'https://maps.googleapis.com/maps/api/streetview?' + urllib.urlencode(data)

    r_metadata = requests.get(url_metadata, allow_redirects=True)

    return (r_metadata.json())


def downloadStreetViewImage(size, lon, lat, heading, pitch, fov, key, directory, filename):
    data = {}
    data['size'] = size
    loc = str(lat) + ',' + str(lon)
    data['location'] = loc
    if heading != 0:  # only non zero heading
        data['heading'] = heading
    data['pitch'] = pitch
    data['fov'] = fov
    data['key'] = key
    url_metadata = 'https://maps.googleapis.com/maps/api/streetview/metadata?' + urllib.urlencode(data)
    url = 'https://maps.googleapis.com/maps/api/streetview?' + urllib.urlencode(data)

    r_metadata = requests.get(url_metadata, allow_redirects=True)

    r_metadata_jason = r_metadata.json()
    print(r_metadata.json())
    print(url)

    filename_jason = directory + '/' + filename + '.json'
    outputfile_json = open(filename_jason, 'w')
    json.dump(r_metadata_jason, outputfile_json)

    retpolepos = {}
    retpolepos['pole'] = {}
    retpolepos['pole']['top'] = {}
    retpolepos['pole']['bottom'] = {}
    retpolepos['pole']['top']['y'] = 0
    retpolepos['pole']['bottom']['y'] = 0
    retpolepos['pole']['bottom']['x'] = 0
    retpolepos['pole']['top']['x'] = 0

    # third party code that detects the pole inthe pciture and makes sure that the whole pole is in the image.
    # I removed this code because it is proprietory and this is a big part of your project
    return retpolepos


def storeCameraPos(camera_pos, heading_from_camera, directory):
    camera_j = {}
    camera_j['lat'] = camera_pos['location']['lat']
    camera_j['lng'] = camera_pos['location']['lng']
    camera_j['poleangle'] = heading_from_camera
    camerafilename = directory + '/' + storefilename + 'camera.json'
    cameraoutputfile = open(camerafilename, 'w')
    json.dump(camera_j, cameraoutputfile)
    return


def ScalePole(polesize, farFromY):
    ScaleAdd = 0
    if farFromY > PoleTop:
        ScaleAdd = 10
    if (polesize < 300):
        return 60 - ScaleAdd
    if (polesize < 500):
        return 65 - ScaleAdd
    if (polesize < 700):
        return 70 - ScaleAdd
    if (polesize < 1000):
        return 80 - ScaleAdd
    if (polesize < 1200):
        return 90 - ScaleAdd
    return 90


def processPole(poleName, poleData):
    centerLat = poleData[1]
    centerLon = poleData[2]
    directory = poleName
    polepos = {}
    polepos['pole'] = {}
    polepos['status'] = 0
    polepos['pole']['top'] = {}
    polepos['pole']['bottom'] = {}
    polepos['pole']['top']['x'] = 0
    polepos['pole']['top']['y'] = 0
    polepos['pole']['bottom']['x'] = 0
    polepos['pole']['bottom']['y'] = 0
    heading_from_camera = 0

    # download the original picture of the pol

    print(poleName, centerLat, centerLon)
    createFolder(directory)
    camera_pos = getCameraPosition(size, centerLon, centerLat, heading, pitch, 80, key)
    if camera_pos['status'] == "OK":
        heading_from_camera = angleFromCoordinate(centerLon, centerLat, camera_pos['location']['lng'],
                                                  camera_pos['location']['lat'])
        # start with a zoomed in image to detect small poles
        polepos = downloadStreetViewImage(size, centerLon, centerLat, heading_from_camera, pitch, 80, key, directory,
                                          storefilename)
        storeCameraPos(camera_pos, heading_from_camera, directory)
    else:
        print("No Camera Picture")

    if ((polepos['status'] != 0) and
            (polepos['pole']['top']['y'] > PoleTop) and
            (polepos['pole']['bottom']['y'] < PoleBottom) and
            (polepos['pole']['bottom']['x'] > TopX) and
            (polepos['pole']['bottom']['x'] < BottomX) and
            (polepos['pole']['top']['x'] > TopX) and
            (polepos['pole']['top']['x'] < BottomX)):
        # zoom only
        fov = ScalePole((polepos['pole']['bottom']['y'] - polepos['pole']['top']['y']),
                        min(polepos['pole']['top']['y'], 2000 - polepos['pole']['bottom']['y']))
        polepos = downloadStreetViewImage(size, centerLon, centerLat, heading_from_camera, pitch, fov, key, directory,
                                          storefilename)
        storeCameraPos(camera_pos, heading_from_camera, directory)
        return

    radius = 0
    while ((polepos['pole']['top']['y'] < TopY) or (polepos['pole']['bottom']['y'] > BottomY) or
           (polepos['status'] == 0) or
           (polepos['pole']['bottom']['x'] < TopX or polepos['pole']['bottom']['x'] > BottomX) or
           (polepos['pole']['top']['x'] < TopX or (polepos['pole']['top']['x'] > BottomX))
    ):
        # very close move away a little bit
        radius = Radius + radius
        if (radius > MAXRADIUS):
            break

        print('Zoomin', radius)

        new_pos = newCoord(centerLon, centerLat, radius, heading_from_camera)
        camera_pos = getCameraPosition(size, new_pos['lon'], new_pos['lat'], heading, pitch, 90,
                                       key)  # When looping zoom out
        if camera_pos['status'] == "OK":
            heading_from_camera = angleFromCoordinate(centerLon, centerLat, camera_pos['location']['lng'],
                                                      camera_pos['location']['lat'])
            polepos = downloadStreetViewImage(size, new_pos['lon'], new_pos['lat'], heading_from_camera, pitch, 90, key,
                                              directory, storefilename)  # When looping zoom out

            if (polepos['pole']['top']['y'] > PoleTop) and (polepos['pole']['bottom']['y'] < PoleBottom):
                # zoom only

                storeCameraPos(camera_pos, heading_from_camera, directory)
                fov = ScalePole((polepos['pole']['bottom']['y'] - polepos['pole']['top']['y']),
                                min(polepos['pole']['top']['y'], 2000 - polepos['pole']['bottom']['y']))
                print(fov)
                polepos = downloadStreetViewImage(size, new_pos['lon'], new_pos['lat'], heading_from_camera, pitch, fov,
                                                  key, directory, storefilename)
                storeCameraPos(camera_pos, heading_from_camera, directory)
            storeCameraPos(camera_pos, heading_from_camera, directory)
        else:
            print("No Camera Picture")
    print("EXIT: ", radius)
    if (radius < MAXRADIUS):  # we foudn the pole
        return
    # Lets zoom out instead on in
    radius = 0
    print("Zoomin out")
    camera_pos = getCameraPosition(size, centerLon, centerLat, heading, pitch, 90, key)
    if camera_pos['status'] == "OK":
        heading_from_camera = angleFromCoordinate(centerLon, centerLat, camera_pos['location']['lng'],
                                                  camera_pos['location']['lat'])
        # start with a zoomed in image to detect small poles
        polepos = downloadStreetViewImage(size, centerLon, centerLat, heading_from_camera, pitch, 100, key, directory,
                                          storefilename)
        storeCameraPos(camera_pos, heading_from_camera, directory)
    else:
        print("No Camera Picture")
    if ((polepos['status'] != 0) and
            (polepos['pole']['top']['y'] > PoleTop) and
            (polepos['pole']['bottom']['y'] < PoleBottom) and
            (polepos['pole']['bottom']['x'] > TopX) and
            (polepos['pole']['bottom']['x'] < BottomX) and
            (polepos['pole']['top']['x'] > TopX) and
            (polepos['pole']['top']['x'] < BottomX)):
        # return  We found a pole
        storeCameraPos(camera_pos, heading_from_camera, directory)
        return
    radius = 0
    while ((polepos['pole']['top']['y'] < TopY) or (polepos['pole']['bottom']['y'] > BottomY) or
           (polepos['status'] == 0) or
           (polepos['pole']['bottom']['x'] < TopX or polepos['pole']['bottom']['x'] > BottomX) or
           (polepos['pole']['top']['x'] < TopX or (polepos['pole']['top']['x'] > BottomX))
    ):
        # very close move away a little bit
        radius = Radius + radius
        if radius > MAXRADIUS:
            return
        print('Zoom out: ', radius)

        new_pos = newCoord(centerLon, centerLat, radius, heading_from_camera)
        camera_pos = getCameraPosition(size, new_pos['lon'], new_pos['lat'], heading, pitch, 100, key)
        if camera_pos['status'] == "OK":
            heading_from_camera = angleFromCoordinate(centerLon, centerLat, camera_pos['location']['lng'],
                                                      camera_pos['location']['lat'])
            polepos = downloadStreetViewImage(size, new_pos['lon'], new_pos['lat'], heading_from_camera, pitch, 90, key,
                                              directory, storefilename)
            print(polepos)
            storeCameraPos(camera_pos, heading_from_camera, directory)
        else:
            print("No Camera Picture")
    return


def main(argv):
    inputfile = '/Users/leon/Downloads/PolesExample.xlsx'
    outputfolder = ''
    options, remainder = getopt.getopt(sys.argv[1:], "hi:", ["ifile="])

    for opt, arg in options:
        if opt in ('-i', '--ifile'):
            inputfile = arg
            print(inputfile)

    my_file = open(inputfile, 'r')
    my_data = np.genfromtxt(inputfile, delimiter=',', skip_header=1)
    my_poles = np.genfromtxt(inputfile, delimiter=',', dtype=None, skip_header=1)
    for rows in range(0, my_data.shape[0]):
        processPole(my_poles[rows][0], my_data[rows])


if __name__ == "__main__":
    main(sys.argv[1:])
