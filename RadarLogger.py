#!/usr/bin/python
import os
import json
import requests
from datetime import datetime, date, time
from pprint import pprint
from subprocess import call

#information about the radar sites:
sitesFile = "/home/pi/RadarLogger/Sites.json"

#information about the users / locations we're interested in.
usersFile = "/home/pi/RadarLogger/Users.json"

#location to save the files
saveRoot = "/home/pi/RadarLogger/archive/"

#prediction engine call
predictor = "/home/pi/SoggyDog/C/SoggyDog"

#output file for settings argument for SoggyDog
predictorSettings = "Paths.json"

#location to save the prediciton files
predictorfolder = "/home/pi/RadarLogger/predictions/"

with open(sitesFile) as sitesJson:
    sites = json.loads(sitesJson.read())
#pprint(sites)


for location in sites['sites']:
    print(location['name'])
    print "lat: " , location['lat']
    print "lon: " , location['lon']
    for loops in location['loops']:
        print(loops['prefix'])
        print(loops['URL'])

        #break it up into folders
        saveDir= saveRoot + location['name'] + "/" + loops['prefix'] + "/"
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

        #fetch the BOM live web-page
        RadarHTML = requests.get(loops['URL'])
        
        #scrape the image URLs from the formatting
        imageUrls = []
        for item in RadarHTML.text.split("\n"):
            if "theImageNames[" in item:
                imageUrls.append(item.split("\"")[1])

        #prepare the arguments for the predictor
        predictorArgs = []
	runPrediction = False
        #download the images
#        for imageUrl in imageUrls:
        for index in range(len(imageUrls)):
            imageUrl = imageUrls[index]
            print(imageUrl)
            path = saveDir + imageUrl.split(".")[5] + ".png"
            print(path)
            #only use the latest two images
            if (index+2) >= len(imageUrls):
                predictorArgs.append(path)
            #print("predictorArgs = " + predictorArgs)

            #only download each one once
            if os.path.exists(path):
                print("skipping")
            else:
                print("downloading")
                #no need to run the predictor on old images
                if (index+2) >= len(imageUrls):
                    runPrediction = True

                #file(filename, 'w').close()
                r = requests.get(imageUrl, stream=True)
                if r.status_code == 200:
                    with open(path, 'wb') as f:
                        for chunk in r.iter_content():
                            f.write(chunk)

        if loops['type'] == 'Rain':
            #build a Paths.json file for SoggyDog:
            with open('Users.json') as usersJson:
                    users = json.loads(usersJson.read())
            with open(predictorSettings, 'w') as pathsjson:
                paths = {'Paths':[], 'Site':{}, 'Conf':{}}

                for place in users['Places']:
                    place['name'] = predictorfolder + place['name'] + ".png"
                    paths['Paths'].append(place)

                #add site info
                paths['Site']['range'] = loops['range']
                paths['Site']['Lat'] = location['lat']
                paths['Site']['Lon'] = location['lon']
                paths['Site']['period'] = location['period']
                #add config info
                paths['Conf']['stepCount'] = 30
                paths['Conf']['stepPeriod'] = 1
                paths['Conf']['maxSpeed'] = 150
                
                json.dump(paths, pathsjson,indent=4)

            #Call SoggyDog
            if runPrediction:
                call([predictor, predictorArgs[0], predictorArgs[1], predictorSettings])
        
exit(0)
