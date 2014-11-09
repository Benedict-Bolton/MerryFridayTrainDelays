from flask import Flask, request, redirect, render_template, session
import json, urllib2

app = Flask(__name__)

origin="Times+Square"
destination="Penn+Station"
arrival_time=1343641500
mapsurl = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&arrival_time=%s&mode=transit&key=AIzaSyBWPZcD2dgi1T0F_dNC1SThe64a-rfdkgY"%(origin,destination,arrival_time)
mapsrequest = urllib2.urlopen(mapsurl)
mapsresult = mapsrequest.read()
mapsD = json.loads(mapsresult)['routes'][0]['legs'][0]['steps'] # a dictionary with api data stuff
for step in mapsD:
    if step['travel_mode']=="TRANSIT":
        train = step['transit_details']['line']['short_name']
        print train

if __name__=="__main__":
    app.debug = True
##    app.run()
