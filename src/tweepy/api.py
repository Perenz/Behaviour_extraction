import tweepy 
import os, json



class TweepyAPI:
    def __init__(self):
        #OAuth2 authentication
        #Get key and secret from the file keys.json
        KEYS = os.path.join(os.path.dirname(__file__), 'keys.json')
        keys = None
        with open(KEYS) as f:
            keys = json.load(f)

        print(keys)

        #Authenticate with key and secret
        self.auth = tweepy.AppAuthHandler(keys['key'], keys['secret'])
        self.api = tweepy.API(self.auth)

    def parse_tweet(self, tweet):
        hashtags = tweet.hashtags
        if hashtags is None:
            hashtags = []
        media = tweet.media
        if media is None:
            media = []
        urls = tweet.urls
        if urls is None:
            urls = []

        return 

    def search(self, query):
        #Search by query and get the results
        return tweepy.Cursor(self.api.search, q="Coronavirus").items(10)

if __name__ == "__main__":
    twApi = TweepyAPI()

    for s in twApi.search("Corona"):
        print(s.text)