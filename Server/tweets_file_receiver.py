from model_manager import run_model_stage


def run_tweets_file_receiver(queue):
    print("started listening to queue")
    while True:
        print("writeBestTweetToFile::Waiting for next tweets file")
        tweets_file = queue.get()
        print("writeBestTweetToFile::Now starting generateTweet " + tweets_file)
        run_model_stage(tweets_file)
