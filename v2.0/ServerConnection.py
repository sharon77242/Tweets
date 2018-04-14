#!/usr/bin/python3

import sys
from flask import Flask, jsonify, url_for

app = Flask(__name__)

bestTweet =  {
        'data': 'Empty tweet',
    }

@app.route('/Tweets/bestTweet', methods=['GET'])
def getBestTweet():
    return jsonify({'bestTweet': bestTweet})

def openServerConnection(bestTweetData, countryName): # country should change the url
    bestTweet['data'] = bestTweetData

    print ('running server connection with tweet: ' + bestTweetData)
    app.run(debug=True) # running on port 5000, curl http://127.0.0.1:5000/Tweets/bestTweet
    
if __name__ == '__main__':
    openServerConnection(sys.argv[1], sys.argv[2]) # arg1 - bestTweet, arg2 - country
