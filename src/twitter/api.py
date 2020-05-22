import tweepy 
import os, json, sys
from itertools import zip_longest

sys.path.insert(0, os.path.abspath(os.getcwd()))
#print(sys.path)

from src.models.twitter import Tweet, User
from src.sentiment.sentiment import SentimentAnalyzer

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


    def get_tweet_list(self, ids):
        '''
            Given a list of integers (ids), return a list of parsed Tweets
        '''

        #TweePy request support max 100 ids
        #Create groups of 100 elements

        groups = list(zip_longest(*[iter(ids)]*100))

        #Can be used as user_timeline for those users already in the dataset
        #giving it the list of all tweets
        toRtn = []
        for g in groups:
            tweets = self.api.statuses_lookup(g, tweet_mode="extended")
            for t in tweets:
                toRtn.append(self.parse_tweet(t))
        
        return toRtn


    def parse_tweet(self, tweet):

        #Should check, I should parse original tweets, replies and quote. 
        #Not retweet without own text
        
        #Get necessary parameters, if the key does not exist, assign empty list [] as default
        #Entities are returned as list. Iterate entities to keep only searched info
        hashtags = [h.get('text') for h in tweet.entities.get('hashtags', [])]   
        mentions = [m.get('id') for m in tweet.entities.get('user_mentions', [])]
        symbols = [s.get('text') for s in tweet.entities.get('symbols', [])]

        place = tweet.place
        if place is None:
            place = {}
        else: 
            #For place, I might by interested in 
            #id?, place_type, full_name or just name
            #bounding_box if there is other way to access coordinates 
            place = {'id':place.id, 'full_name':place.full_name, 'place_type':place.place_type}
        
        

        '''
        to catch retweets:
            Retweeted post without new text is a RETWEET
            Retweeted post with new text is a QUOTE
            Replied is a REPLY
        '''
        #0 for Original tweets, 1 for Replies, 2 for Retweets, 3 for quotes

        #Set tweet_type
        tweet_type=0 #DEFAULT
        if tweet.in_reply_to_status_id is not None: #Check for replies
            tweet_type=1
        elif hasattr(tweet, 'retweeted_status'): #Check for retweets
            tweet_type=2
        elif tweet.is_quote_status: #Check for quotes
            tweet_type=3

        try:
            text = tweet.retweeted_status.full_text
            #For media use extended_entitities because entities contain only the first media uploaded in the tweet
            media = tweet.retweeted_status.extended_entities.get('media', [])
            urls = [u.get('expanded_url') for u in tweet.retweeted_status.entities.get('urls', [])]
            #Should get all the information (id, fav, media, urls, ...) from the original tweet?
            #Not ID, Created_at
        except:
            text = tweet.full_text
            urls = [u.get('expanded_url') for u in tweet.entities.get('urls', [])]
            try: 
                #If tweets has more than 1 media, it is necessary to use extended_entities
                media = tweet.extended_entities.get('media', [])
            except:
                media = tweet.entities.get('media',[])
        

        #Per Media sono interessato a media_url, type
        media = [{'type':m.get('type'), 'media_url':m.get('media_url')} for m in media]

        return Tweet(tweet.id,text,tweet.favorite_count, hashtags, media, tweet.retweet_count, urls, tweet.created_at, mentions, symbols, place, tweet_type)


    def parse_user(self, user):
        #Necessary parameters: id, name, location, description, verified, followers_count, friends_count, listed_count, favourites_count, statuses_count
        return User(user.id, user.name, user.location, user.description, user.verified, user.followers_count, user.friends_count, user.listed_count, user.favourites_count)


    def search(self, query):
        #Search by query and get the results
        return tweepy.Cursor(self.api.search, q="Coronavirus").items(10)


    def get_user(self, screen_name):
        return self.parse_user(self.api.get_user(screen_name))

    def get_user_timeline(self, userID, since=None):
        #Number of requested status
        #Each request allow a max of 200
        StatusNumber = 20
        count = 20 #It must be less equal than 200
        count=min(count, StatusNumber)
        offset = StatusNumber % count
        #List of the whole timeline
        timeline = []
        #Id of the oldest tweet
        lastId = 0

        #Check offset value in order to handle problem with lastID undefined
        if offset == 0:
            lastId = self.api.user_timeline(userID, count=1, tweet_mode="extended")[-1].id +1 #+1 to make sure this single status will be caught by the next user_timeline call
        else:
            #Get the first 'offest' elements and assign the lastID
            timeline.extend(self.api.user_timeline(userID, since_id=since, count=offset, tweet_mode="extended"))
            #Because of since_id, the returned list could be empty
            try:
                lastId=timeline[-1].id #Last element of the retrieved list is the oldest one
            except:
                #If it's empty, there are no new activities
                return []

        #Iterate statusNumber//count times, each time get #count tweets
        for i in range(StatusNumber//count):      
            timeline.extend(self.api.user_timeline(userID, since_id=since, count=count, max_id=lastId-1, tweet_mode="extended"))
            #update last tweet's ID
            try:
                lastId=timeline[-1].id
            except:
                return []

        #Parse all the obtained status with the class Tweet
        parsed_timeline = [self.parse_tweet(t) for t in timeline]
        return parsed_timeline

    
    def user_from_repr(self, data):
        return User.from_repr(data)

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
    #test 551190807

    name = 'SPerenzoni'
    user = twApi.get_user(name)
    timeline = twApi.get_user_timeline(name)

    user.set_tweets(timeline)

    #print(user)
    user.to_json()


    '''
    Different steps:
        - Retrieve User from Twitter
        - Retrieve his/her timeline

        -Compute aggregate data
    
        -Compute sentiment and aggregate sentiment
        -Together there will be also the Semantic
    '''

    '''
    for t in tmp:
        print(t)
    '''
    '''Aknowledgements
        In retweets media are not caught 
    '''