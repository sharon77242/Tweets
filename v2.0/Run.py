#!/usr/bin/python3
import subprocess
from TweetsCountry import mineTweets

if __name__ == "__main__":
	tweetsFile = TweetsCountry.mineTweets()
	print ('saved tweets file: ' + tweetsFile)
	#subprocess.call(["python3 /home/project45/Tweets_From_Git/Tweets/v2.0/TweetsCountry.py"], shell =True)
	#subprocess.call("/home/project45/Tweets_From_Git/Tweets/v2.0/learn.py")
	subprocess.call(["python /home/project45/Tweets_From_Git/Tweets/v2.0/generator.py models/model.pickle models/lang.pickle"], shell =True)
