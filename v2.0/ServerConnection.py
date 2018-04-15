#!/usr/bin/python3

import sys
import os
from flask import Flask, jsonify, url_for

app = Flask(__name__)

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

@app.route('/Tweets/<country>', methods=['GET'])
def getBestTweet(country):
    bestTweet['data'] = readBestTweetFromFile(country)
    return jsonify({'bestTweet': bestTweet})

def openServerConnection():
    app.run(debug=True) # running on port 5000, curl http://127.0.0.1:5000/Tweets/california
    
if __name__ == '__main__':
    openServerConnection()
