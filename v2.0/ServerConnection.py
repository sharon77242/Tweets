#!/usr/bin/python3

import os
from flask import Flask, jsonify, url_for, request, json
from flask_cors import CORS

''' 
file names example : california_21_04_2018_18_19
                    <country>_day_month_year_hour_minute
running on port 5000,
curl http://127.0.0.1:5000/california  ,
curl -H "Content-Type: application/json" -X POST -d '{"country":"california","time":"21_04_2018_18_19"}' http://127.0.0.1:5000/
'''

app = Flask(__name__)
CORS(app)

bestTweet = {
        'data': 'Empty tweet',
    }


def read_times_on_country_from_file(country):
    data = []
    for fileName in os.listdir('bestTweets/'):
        if country in fileName:
            data.append((fileName.split(country, 1)[1])[1:])
    if data:
        return data
    return [' error - the tweet file doesnt exists its probably still learning']


def read_best_tweet_from_file(country, time):
    with open('bestTweets/' + country + '_' + time, 'r') as tweetFile:
        data = tweetFile.read()
        return data.rstrip()
    return ' error - the tweet file doesnt exists its probably still learning'


@app.route('/<country>', methods=['GET'])
def get_times_for_country(country):
    return jsonify(read_times_on_country_from_file(country))


@app.route('/', methods=['POST'])
def get_best_tweet_for_country_and_time():
    if request.method == 'POST':
        country = request.json['country']
        time = request.json['time']
        return jsonify(read_best_tweet_from_file(country, time))


def open_server_connection():
    app.run(debug=False)


if __name__ == '__main__':
    open_server_connection()