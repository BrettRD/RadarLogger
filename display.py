
import json
from datetime import datetime, date, time
from pprint import pprint



def genhtml (imagelist):
    html  = "<!DOCTYPE html>"
    html += "<html>"
    html += "<body>"
    html += "<h2>SoggyDog</h2>"
    html += "<h3>Dubious Local Weather Predictions</h3>"
    html += "<p>"
    for place in imagelist['Paths']:
        #html += "<h3>" + place['name'] + "</h3>" 
        #html += "Lat = " + str(place['Lat']) + "<br>Lon = " + str(place['Lon']) + "<br>"
        #html += "Vaild as of " + imagelist['Site']['time'] + " UTC<br>"
        #html += "<img src=\"" + place['WebFile'] + "\" alt=\"Prediction for "+ place['name'] + "\" width=\"50%\"><br>"
        #html += "Generated from <a href=\"" + imagelist['Site']['URL'] + "\">" + imagelist['Site']['name'] + " " + imagelist['Site']['prefix'] + "</a><br>"
        #html += "<br><br>"
        html += "<a href=\"" + place['name']+".html" + "\">" + place['name'] + "</a><br>"
        #html += "<br><br>"
    html += "</p>"
    html += "</p>"
    html += "</body>"
    html += "</html>"

    return html

def genPredictionPage (imagelist, place):
    validyear = imagelist['Site']['time'][0:4]
    validmonth = imagelist['Site']['time'][4:6]
    validdate = imagelist['Site']['time'][6:8]
    validhour = imagelist['Site']['time'][8:10]
#    validhour = str(8 + int(imagelist['Site']['time'][8:10])) #hax
    validminute = imagelist['Site']['time'][10:12]
    validDatestring =  str(validyear) + "-" + str(validmonth) + "-" + str(validdate) + "T" + str(validhour) + ":" + str(validminute) + ":00+00:00"
    imgpxWidth = 20
    imgWidth = imgpxWidth*imagelist['Conf']['stepCount']
    flowimgwidth = 100
    html  = "<!DOCTYPE html>"
    html += "<html>"
    html += "<head>"
    html += "<style type=\"text/css\">"
    html += "table td{"
    html += "    border:none;"
    html += "    padding:0px;"
    html += "}"
    html += "table{"
    html += "    border:none;"
    html += "    border-collapse:collapse;"
    html += "    border-spacing:0px;"
    html += "}"
    html += "</style>"
    html += "</head>"
    html += "<body>"
    #valiables
    html += "<script>\n"
    html += "validFrom = new Date(\"" + validDatestring + "\");\n"
    #html += "validFrom = Date.parse(\"" + validDatestring + "\");\n"
    html += "stepCount = " + str(imagelist['Conf']['stepCount'])   + "; //number of time steps in the prediciton\n"
    html += "stepPeriod = " + str(imagelist['Conf']['stepPeriod']) + "; //lenght of each time step in minutes\n"
    html += "width = " + str(imgpxWidth) + "*stepCount;    //width of the prediciton image in px\n"
    html += "length = stepCount*stepPeriod*60; //length of the prediciton in seconds\n"
    html += "</script>\n"

    #utility script
    html += "<script>\n"
    html += "function init(){\n"
    html += "    timePtr = document.getElementById('nowMark');\n"
    html += "    timePtr.style.position= 'relative';\n"
    html += "    timePtr.style.left = '0px'; \n"
    html += "    timePtr.innerHTML = \"^\"; \n"
    html += "    refreshDate();\n"
    html += "}\n"
    html += "function refreshDate(){\n"
    html += "    var d = new Date();\n"
#    html += "    document.getElementById(\"timer\").innerHTML = d.getTime() - validFrom.getTime();\n"
    html += "    var sec = Math.round((d.getTime() - validFrom.getTime())/1000);\n"
#    html += "    var sec = Math.round((d.UTC() - validFrom)/1000);\n"
#    html += "    document.getElementById(\"timer\").innerHTML = \"Seconds since prediciton: \" + sec;\n"
    html += "    timePtr.style.left = width*sec/length + 'px';\n"
    html += "}\n"
    html += "window.onload = init;\n"
    html += "setInterval(refreshDate, 1000);\n"
    html += "</script>\n"




    #display stuff
    html += "<h2>SoggyDog Prediction Results</h2>\n"
    html += "<p>\n"
    
    html += "<h3>" + place['name'] + "</h3>\n"
    html += "<table>"
    html += "<tr><td style=\"width:" + str(imgpxWidth + imgWidth - flowimgwidth) + "px;\">" 
    html += "Lat = " + str(place['Lat']) + "<br>Lon = " + str(place['Lon']) + "<br>\n"
    html += "Vaild as of " + imagelist['Site']['time'] + " UTC\n"
    html += "</td>"

    html += "<td style=\"width:" + str(flowimgwidth) + "px;\"><img src=\"" + imagelist['Site']['WebFlowFile'] + "\" alt=\"Wind Estimate\" width=\"" + str(flowimgwidth) + "\" >\n</td></tr>"

    html += "<tr><td colspan=\"2\" style=\"width:" + str(imgpxWidth + imgWidth) + "px;\">"
    html += "<img src=\" Legend.png \" width=\"" + str(imgpxWidth) + "\">"
    html += "<img src=\"" + place['WebFile'] + "\" alt=\"Prediction for "+ place['name'] + "\" width=\"" + str(imgWidth) + "\">\n"
    #html += "<p id=\"nowMark\">^</p>\n"
    html += "<p id=\"nowMark\"></p>\n"
    html += "</td></tr></table>"
    html += "Generated from <a href=\"" + imagelist['Site']['URL'] + "\">" + imagelist['Site']['name'] + " " + imagelist['Site']['prefix'] + "</a><br>\n"
    html += "<br><br>\n"
    html += "</p>\n"
    #html += "<p id=\"timer\"></p>\n"
    html += "</body>\n"
    html += "</html>\n"

    return html
