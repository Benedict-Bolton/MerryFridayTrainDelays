from flask import Flask, request, redirect, render_template, session
import json, urllib2
from math import pow

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=="GET":
        return render_template('home.html')
    else:
        origin = request.form['start'].replace(' ','+')
        print origin
        destination= request.form['end'].replace(' ','+')
        print destination
        arrival_time=1343641500
        mapsurl = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&arrival_time=%s&mode=walking&key=AIzaSyBWPZcD2dgi1T0F_dNC1SThe64a-rfdkgY"%(origin,destination,arrival_time)
        mapsrequest = urllib2.urlopen(mapsurl)
        mapsresult = mapsrequest.read()
        try:
            mapsD = json.loads(mapsresult)['routes'][0]['legs'][0] # a dictionary with api data stuff
        except:
            return render_template('home.html') ## error handling in case google maps can't find path from start to end
        start_lat = mapsD['start_location']['lat']
        print start_lat
        start_lng = mapsD['start_location']['lng']
        print start_lng
        end_lat = mapsD['end_location']['lat']
        print end_lat
        end_lng = mapsD['end_location']['lng']
        print end_lng

        elevurl = "https://maps.googleapis.com/maps/api/elevation/json?locations=%f,%f|%f,%f&key=AIzaSyBWPZcD2dgi1T0F_dNC1SThe64a-rfdkgY"%(start_lat,start_lng,end_lat,end_lng)
        elevrequest = urllib2.urlopen(elevurl)
        elevresult = elevrequest.read()
        elevD = json.loads(elevresult)['results']
        start_elev = elevD[0]['elevation'] # in meters
        print start_elev
        end_elev = elevD[1]['elevation'] # in meters
        print end_elev

        ##weight calculations
        G = 6.67384*pow(10,-11)
        M = 5.9726*pow(10,24)
        m = int(request.form['weight']) ##should be an float/int
        R = 6371000
        weight_initial = (G*M*m)/pow(R+start_elev,2)
        weight_final = (G*M*m)/pow(R+end_elev,2)
        ##final-initial = change, so initial-final = loss, i think
        print weight_initial/m
        print weight_final/m
        loss = weight_initial-weight_final # in Newtons
        loss = loss / 4.44822162825 # in pounds
        loss = loss * 1000 # in more impressive pounds
        return render_template('results.html',loss=loss)

if __name__=="__main__":
    app.debug = True
    app.run()
