import tweepy 
import os, json, sys

sys.path.insert(0, os.path.abspath(os.getcwd()))
print(sys.path)

from src.struct.twitter import Tweet, User

class TweepyAPI:
    def __init__(self):
        #OAuth2 authentication
        #Get key and secret from the file keys.json
        KEYS = os.path.join(os.path.dirname(__file__), 'keys.json')
        keys = None
        with open(KEYS) as f:
            keys = json.load(f)

        #Authenticate with key and secret
        self.auth = tweepy.AppAuthHandler(keys['key'], keys['secret'])
        self.api = tweepy.API(self.auth)

    def parse_tweet(self, tweet):
        #Get necessary parameters, if the key does not exist, assign empty list [] as default
        hashtags = tweet.entities.get('hashtags', [])
        media = tweet.entities.get('media', [])
        urls = tweet.entities.get('urls', [])

        place = tweet.place
        if place is None:
            place = []
        else:  
            place = place.full_name

        print(place)

        return Tweet(tweet.id,tweet.text,tweet.favorite_count, hashtags, media, tweet.retweet_count, urls, place, tweet.created_at)

    def parse_user(self, user):
        #Necessary parameters: id, name, location, description, verified, followers_count, friends_count, listed_count, favourites_count, statuses_count
        return User(user.id, user.name, user.location, user.description, user.verified, user.followers_count, user.friends_count, user.listed_count, user.favourites_count, user.statuses_count)

    def search(self, query):
        #Search by query and get the results
        return tweepy.Cursor(self.api.search, q="Coronavirus").items(10)

    def get_user(self, screen_name):
        return self.parse_user(self.api.get_user(screen_name))

    def get_user_timeline(self, userID):
        #Number of requested status
        #Each request allow a max of 200
        StatusNumber = 21
        count = 10 #It must be less equal than 200
        offset = StatusNumber % count
        #List of the whole timeline
        timeline = []
        #Id of the oldest tweet
        lastId = 0

        #Check offset value in order to handle problem with lastID undefined
        if offset == 0:
            lastId = self.api.user_timeline(userID, count=1)[-1].id #+1 to make sure this single status will be caught by the next user_timeline call
        else:
            #Get the first 'offest' elements and assign the lastID
            timeline.extend(self.api.user_timeline(userID, count=offset))
            lastId=timeline[-1].id #Last element of the retrieved list is the oldest one
        

        #Iterate statusNumber//count times, each time get #count tweets
        for i in range(StatusNumber//count):      
            timeline.extend(self.api.user_timeline(userID, count=count, max_id=lastId-1))
            #update last tweet's ID
            lastId=timeline[-1].id

        #Parse all the obtained status with the class Tweet
        parsed_timeline = [self.parse_tweet(t) for t in timeline]
        return parsed_timeline

if __name__ == "__main__":
    twApi = TweepyAPI()

    '''
    #Example of search by query "Corona"
    for s in twApi.search("Corona"):
        print(s.text)
    '''

    #Example of search of a specific user and his/her tweets
    '''
    for t in (twApi.get_user_timeline((twApi.get_user("StephenCurry30").id))):
        print(twApi.parse_tweet(t))
    '''
    #42562446 is Stephen Curry's ID
    #1093586351549804544 Stefano Perenzoni (SPerenzoni)'s ID
    #2250682499 Raffaele Pojer (raffaelepojer)'s ID
    print(twApi.get_user("SPerenzoni"))
    tmp = twApi.get_user_timeline("SPerenzoni")
    for t in tmp:
        print(t)