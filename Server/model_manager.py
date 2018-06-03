from model_learner import learn
from model_generator import generateBestTweet
from os.path import basename
from constants import BEST_TWEETS


def write_best_tweet_to_file(best_tweet, tweets_file):
    tweets_file = basename(tweets_file)  # Get file name from file path
    tweets_file = tweets_file.replace(" ", "_")  # Change ' ' to '_'
    tweets_file = tweets_file[7:]
    with open(BEST_TWEETS + '/' + tweets_file, 'w') as tweetFile:
        tweetFile.write(best_tweet)


def run_model_stage(tweets_file):
    print('starting to learn model on file: ' + tweets_file)
    model, lang = learn(tweets_file)
    print('saved model named: ' + model)
    print('saved lang named: ' + lang)

    best_tweet = generateBestTweet(model, lang)
    print('best tweet is: ' + best_tweet)

    write_best_tweet_to_file(best_tweet, tweets_file)
