#!/usr/bin/python
import os
import json
import requests
from datetime import datetime, date, time
from pprint import pprint
from subprocess import call
from display import genhtml, genPredictionPage

#information about the radar sites:
sitesFile = "/home/pi/RadarLogger/Sites.json"

#information about the users / locations we're interested in.
usersFile = "/home/pi/RadarLogger/Users.json"

#location to save the files
saveRoot = "/home/pi/RadarLogger/archive/"

#prediction engine call
predictor = "/home/pi/SoggyDog/C/SoggyDog"

#output file for settings argument for SoggyDog
predictorSettings = "/home/pi/RadarLogger/Paths.json"


#file system location for the output data
webroot = "/var/www/"

htmlfile = webroot + "soggydog.html"

#location to add to the url
webfolder = "predictions/"

#location to save the prediciton files
predictorfolder = webroot + webfolder
#predictorfolder = "/home/pi/RadarLogger/predictions/"


with open(sitesFile) as sitesJson:
    sites = json.loads(sitesJson.read())
    sitesJson.close()
#pprint(sites)


for location in sites['sites']:
#    print(location['name'])
#    print "lat: " , location['lat']
#    print "lon: " , location['lon']
    for loops in location['loops']:
#        print(loops['prefix'])
#        print(loops['URL'])

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
            timestamp = imageUrl.split(".")[5]
            path = saveDir + timestamp + ".png"
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
                        f.close()

        if loops['type'] == 'Rain':
            #build a Paths.json file for SoggyDog:
            with open(usersFile) as usersJson:
                users = json.loads(usersJson.read())
                
                paths = {'Paths':[], 'Site':{}, 'Conf':{}}

                for place in users['Places']:
                    imgName = place['name'] + timestamp + ".png"
                    place['OutFile'] = predictorfolder + imgName
                    place['WebFile'] = webfolder + imgName
#                    place['OutFile'] = predictorfolder + place['name'] + timestamp + ".png"
                    paths['Paths'].append(place)

                #add site info
                paths['Site']['range'] = loops['range']
                paths['Site']['URL'] = loops['URL']
                paths['Site']['prefix'] = loops['prefix']
                paths['Site']['description'] = loops['description']
                paths['Site']['name'] = location['name']
                paths['Site']['Lat'] = location['lat']
                paths['Site']['Lon'] = location['lon']
                paths['Site']['period'] = location['period']
                paths['Site']['time'] = timestamp
                paths['Site']['FlowFile'] = predictorfolder + loops['prefix'] + "Flow" + timestamp + ".png"


                #add config info
                paths['Conf']['stepCount'] = 30
                paths['Conf']['stepPeriod'] = 1
                paths['Conf']['maxSpeed'] = 150
                
            with open(predictorSettings, 'w') as pathsjson:
                json.dump(paths, pathsjson,indent=4)
                pathsjson.close()
            #Call SoggyDog
            if runPrediction:
                call([predictor, predictorArgs[0], predictorArgs[1], predictorSettings])
                #call(predictor, predictorArgs[0], predictorArgs[1], predictorSettings)
                
            print("Generating landing page")
            #Update the webpage
            html = genhtml(paths)
            with open(htmlfile, 'w') as displayfile:
                displayfile.write(html)
                displayfile.close()
    
            print("Generating place pages")
            for place in paths['Paths']:
                placeFile = webroot + place['name'] + ".html"
                html = genPredictionPage(paths, place)
                with open(placeFile, 'w') as displayfile:
                    displayfile.write(html)
                    displayfile.close()


        
exit(0)
