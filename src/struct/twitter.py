from src.sentiment.sentiment import SentimentAnalyzer
from src.support.data_cleaning import *
from typing import List

class User:
    '''
        Class that represent needed parameters of a user
    '''

    def __init__(self, id, name, location, description, verified, followers, following, listed, favorites, status):
        '''
           parameters:
           verified: a boolean true or false
           followers: total number of followers
           following: total number of "followings"
           listed: total number of public lists that this user is a member of
           favorites: Total number of tweets this user has liked
           status: Total number of tweets (including retweets)
        '''
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.verified = verified
        self.followers = followers
        self.following = following
        self.listed = listed
        self.favorites = favorites
        self.status = status
        self.timeline = None

    def set_tweets(self, tweets):
        tweets_number = len(tweets)
        self.timeline = {'timeline':tweets, 'tweets_number':tweets_number}
        #Init to 0 counter of objective ans subjective tweets
        obj = subj = 0
        polarity = 0

        #Compute aggregate subjectivity and polarity
        for t in tweets:
            sentiment = t.sentiment
            #Compute subjectivity
            if sentiment['type'] == 'neutral':
                obj += 1
            else:
                #If tweet is either positive or negative
                subj += 1
            
            #Compute polarity
            polarity += sentiment['score']

        #Handle only subj tweets
        try:
            sent = subj/obj
        except:
            sent = subj

        #TODO handle 0 tweets
        #Subjectivity represents the ratio of pos/neg tweet with neutral ones
        self.sentiment = {'subjectivity':round(sent, 2), 'polarity':round(polarity/tweets_number, 2)}
       

    def __repr__(self):
        return 'User(id = {id},' \
               ' name = {name},' \
                ' followers = {followers},' \
                ' following = {following},' \
                ' listed = {listed},' \
                ' favorites = {fav},' \
                ' verified = {ver}' \
                ' number of tweets = {tweets_num}\n' \
                'sentiment = {sent}'.format(
                    id=self.id,
                    name=self.name,
                    fav=self.favorites,
                    followers = self.followers,
                    following = self.following,
                    listed = self.listed,
                    ver = self.verified,
                    sent = self.sentiment,
                    tweets_num = self.timeline['tweets_number']
                )

    # Comparison based on the user ID. 
    def __eq__(self, u):
        return self.id == u.id

    def __lt__(self, u):
        return self.id < u.id

    def __gt__(self, u):
        return self.id > u.id

    def __hash__(self):
        return self.id  

class Tweet:
    '''
        Class that represent needed parameters of a tweet
    '''

    def __init__(self, id, text, favorite, hashtags, media, retweet_count, urls, coordinates, created_at, mentions):
        '''
        Parameters:
        favorite: totaln number of favorite 
        hashtags: Array of strings containing all the hashtags
        media: Array of link to the media attached to the tweet
        url: array of links the tweet contains
        '''
        self.id = id
        self.text = text_cleaner(text)
        self.favorite = favorite
        self.hashtags = hashtags
        self.media = media
        self.retweet_count = retweet_count
        self.urls = urls
        self.mentions = mentions
        self.coordinates = coordinates
        self.created_at = created_at

        self.sentApi = SentimentAnalyzer()

        #Call the method for the computation of the sentiment values
        self.__compute_sentiment()
        #self.sentiment=0

    def __repr__(self):
        return '(Tweet(id = {id},' \
               ' text = {text},' \
               ' created_at = {created_at},' \
               ' favorite_count = {fav},' \
               ' retweet_count = {ret},' \
               ' hashtags = {hashtags},' \
                ' media = {media},' \
                ' urls = {urls},' \
                ' mentions = {mentions},' \
                ' sentiment = {sent},' \
                ' coordinates = {coor})'.format(
                    id=self.id,
                    text=self.text,
                    ret=self.retweet_count,
                    fav=self.favorite,
                    coor=self.coordinates,
                    created_at = self.created_at,
                    hashtags = self.hashtags,
                    media = self.media,
                    urls = self.urls,
                    sent = self.sentiment,
                    mentions = self.mentions
                )

            
    def __compute_sentiment(self):
        #Send the request
        response = self.sentApi.text_request(self.text)
        '''
            Response has the following parameters:
                timestamp, time, lang, langConfidence, sentiment: {type, score}
        '''

        self.sentiment = response.get('sentiment')


    # Comparison based on the tweet ID. the greater it is, the older the tweet is
    def __eq__(self, t):
        return self.id == t.id

    def __lt__(self, t):
        return self.id < t.id

    def __gt__(self, t):
        return self.id > t.id

    def __hash__(self):
        return self.id
