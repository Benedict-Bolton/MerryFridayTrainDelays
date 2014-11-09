from flask import Flask, request, redirect, render_template, session
import json, urllib2

app = Flask(__name__)

origin="Times+Square"
destination="Penn+Station"
arrival_time=1343641500
mapsurl = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&arrival_time=%s&mode=transit&key=AIzaSyBWPZcD2dgi1T0F_dNC1SThe64a-rfdkgY"%(origin,destination,arrival_time)
mapsrequest = urllib2.urlopen(mapsurl)
mapsresult = mapsrequest.read()
mapsD = json.loads(mapsresult)['routes'][0]['legs'][0] # a dictionary with api data stuff
start_lat = mapsD['start_location']['lat']
start_lng = mapsD['start_location']['lng']
end_lat = mapsD['end_location']['lat']
end_lng = mapsD['end_location']['lng']

elevurl = "https://maps.googleapis.com/maps/api/elevation/json?locations=%f,%f|%f,%f&key=AIzaSyBWPZcD2dgi1T0F_dNC1SThe64a-rfdkgY"%(start_lat,start_lng,end_lat,end_lng)
elevrequest = urllib2.urlopen(elevurl)
elevresult = elevrequest.read()
elevD = json.loads(elevresult)['results']
start_elev = elevD[0]['elevation'] # in meters
end_elev = elevD[1]['elevation'] # in meters
print `start_elev`+', '+`end_elev`

if __name__=="__main__":
    app.debug = True
##    app.run()
