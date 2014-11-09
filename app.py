from flask import Flask, request, redirect, render_template, session
import json, urllib2
from math import pow

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=="GET":
        return render_template('home.html')
    else:
        origin = request.form['start']
        destination= request.form['end']
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

        ##weight calculations
        G = 6.67*pow(10,-11)
        M = 5.97*pow(10,24)
        m = request.form['weight'] ##should be an float/int
        R = 6371000
        weight_initial = (G*M*m)/pow(R+start_elev,2)
        weight_final = (G*M*m)/pow(R+end_elev,2)
        ##final-initial = change, so initial-final = loss, i think
        return render_template('results.html',loss=(weight_initial-weight_final))

if __name__=="__main__":
    app.debug = True
    app.run()
