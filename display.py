
import json
from datetime import datetime, date, time
from pprint import pprint



def genhtml (imagelist):
    html  = "<!DOCTYPE html>"
    html += "<html>"
    html += "<body>"
    html += "<h2>SoggyDog Prediction Results</h2>"
    html += "<p>"
    for place in imagelist['Paths']:
        html += "<h3>" + place['name'] + "</h3>" 
        html += "Lat = " + str(place['Lat']) + "<br>Lon = " + str(place['Lon']) + "<br>"
        html += "Vaild as of " + imagelist['Site']['time'] + " UTC<br>"
        html += "<img src=\"" + place['WebFile'] + "\" alt=\"Prediction for "+ place['name'] + "\" width=\"50%\"><br>"
        html += "Generated from <a href=\"" + imagelist['Site']['URL'] + "\">" + imagelist['Site']['name'] + " " + imagelist['Site']['prefix'] + "</a><br>"
        html += "<br><br>"
    html += "</p>"
    html += "</body>"
    html += "</html>"

    return html

