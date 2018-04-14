#!/usr/bin/python3

from TweetsCountry import mineTweets
from learn import learn
from generator import generateBestTweet
from ServerConnection import openServerConnection
from multiprocessing import Process
import time

c_new_york = 'new york'
c_locations_new_york = [c_new_york, 'nyc', ' ny']

c_los_angeles = 'los angeles'
c_locations_los_angeles = [c_los_angeles, ', la']

c_california = 'california'
c_locations_california = [c_california, ', ca ']
	
countries = [c_locations_new_york, c_locations_los_angeles, c_locations_california]

def run(country):
	try:
		tweetsFile = mineTweets(country, 0.05)
		print ('saved tweets file: ' + tweetsFile)

		model, lang = learn(tweetsFile)
		print ('saved model named: ' + model)
		print ('saved lang named: ' + lang)

		bestTweet = generateBestTweet(model,lang)
		print ('best tweet is: ' + bestTweet)

		openServerConnection(bestTweet, country[0])

	except (KeyboardInterrupt, SystemExit):
		print ('Process of Country:' + country[0] + ' Exit')
	
if __name__ == "__main__":

	for country in countries:	
		time.sleep(2)
		p = Process(target=run, args=(country,))
		p.start()
		#p.join()
		
