#!/usr/bin/python3

import sys
import os
from flask import Flask, jsonify, url_for, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bestTweet =  {
        'data': 'Empty tweet',
    }

def readBestTweetFromFile(country):
    for fileName in os.listdir('bestTweets/'):
         if country in fileName: 
              with open('bestTweets/' + fileName, 'r') as tweetFile:
                   data = tweetFile.read()
              return data
    return 'error - the tweet file doesnt exists its probably still learning'

@app.route('/<country>', methods=['GET'])
def getTimesForCountry(country):
    return jsonify(['21/04/2018 18:19', '21/04/2018 19:19', '21/04/2018 20:19'])

@app.route('/', methods=['POST'])
def getBestTweetForCountryAndTime():
    if request.method == 'POST':
        country = request.form['country']
        time = request.form['time']

def openServerConnection():
    app.run(debug=True) # running on port 5000, curl http://127.0.0.1:5000/california
    
if __name__ == '__main__':
    openServerConnection()
