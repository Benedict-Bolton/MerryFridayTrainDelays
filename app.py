from flask import Flask, request, redirect, render_template, session
import json, urllib2

app = Flask(__name__)

url = "" #insert api url here
request = urllib2.urlopen(url)
result = request.read()
d = json.loads(result) # a dictionary with api data stuff

if __name__=="__main__":
    app.debug = True
    app.run()
