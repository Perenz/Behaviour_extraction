from src.sentiment.sentiment import SentimentAnalyzer
from src.support.data_cleaning import *
from datetime import datetime
from typing import List

import json

class User:
    '''
        Class that represent needed parameters of a user
    '''

    def __init__(self, id, name, location, description, verified, followers, following, listed, favorites, status=0, last=None, timeline=[]):
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
        self.tweets_number=status
        self.last=last
        if timeline == []:
            self.timeline = []
        else:
            self.timeline = timeline

    def add_tweets(self, tweets):
        tweets_number = len(tweets)
        #self.timeline = {'timeline':tweets, 'tweets_number':tweets_number}  
        if tweets_number>0:
            self.timeline += tweets
            self.last = max(t.id for t in tweets)
            self.tweets_number += tweets_number

        '''
        Move this in compute aggregates
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
        self.sentiment = {'subjectivity':round(sent, 3), 'polarity':round(polarity/tweets_number, 3)}
        #Call the method to compute the aggreagate values
        self.__compute_aggregates()
        '''



    def __compute_aggregates(self):
        '''
            Private method that given a user full of its timeline extract the hashtags, mentions, url
            A dict key-value and also metadata (total number, avg per tweet)
        '''
        #Should then be moved above in set_tweet to avoid a double loop over all tweets
        #Media should be taken by extended_entities
        #hashtags, media, mentions and url are all array of this entity

        #Hashtags, urls, mentions, media (Could be divided), symbols

        #for each tweet
        hash_dict = dict()
        hash_dict['occurrences'] = dict()
        hash_dict['num_hashtags'] = 0

        mentions = dict()
        urls = dict()
        mentions['occurrences'] =  dict()
        urls['occurrences'] = dict()
        mentions['num_mentions'] = urls['num_urls'] = 0

        media = dict()
        media['occurrences']=dict()
        media['num_media']=0

        symbols = dict()
        symbols['occurrences']=dict()
        symbols['num_symbols']=0

        self.timeline['favorite_count'] = 0
        self.timeline['retweet_count'] = 0
        for t in self.timeline['timeline']:
            #List of all the IDs
            #HASHTAGS
            hash_dict['num_hashtags'] += len(t.hashtags)
            for h in t.hashtags:
                #Hashtags are not case-sensitive, dicts are, so put everything to lowercase
                text = h.get('text').lower()
                hash_dict['occurrences'][text] = hash_dict['occurrences'].get(text, 0) + 1

            #USER_MENTIONS (mentions)
            mentions['num_mentions'] += len(t.mentions)
            for m in t.mentions:
                #Not Case-sensitive
                text = m.get('screen_name').lower()
                mentions['occurrences'][text] = mentions['occurrences'].get(text,0) + 1

            #URLS (urls)
            urls['num_urls'] += len(t.urls)
            for u in t.urls:
                #There are 'url, 'display_url', 'expanded_url'
                #Case sensitive
                text = u.get('url') #url in the form http://t.co/IOwBrTZR
                urls['occurrences'][text] = urls['occurrences'].get(text,0)+1

            #MEDIA (media)
            media['num_media'] += len(t.media)
            for m in t.media:
                #media_url is case sensitive
                #'type' could be interesting: photo, video, animated_gif
                text = m.get('media_url')
                media['occurrences'][text] = media['occurrences'].get(text,0)+1

            #SYMBOLS (symbols)
            symbols['num_symbols'] += len(t.symbols)
            for s in t.symbols:
                #symbols 'text
                text = s.get('text')
                print(text) #DEBUG
                symbols['occurrences'][text] = symbols['occurrences'].get(text,0)+1

            #Total favorite and retweet
            self.timeline['favorite_count'] += t.favorite
            self.timeline['retweet_count'] += t.retweet_count
                


        tweets_number = self.timeline['tweets_number']
        hash_dict['hashtags_per_tweet'] = round(hash_dict['num_hashtags'] / tweets_number, 3)
        mentions['mentions_per_tweet'] = round(mentions['num_mentions'] / tweets_number, 3)
        urls['urls_per_tweet'] = round(urls['num_urls'] / tweets_number, 3)
        media['media_per_tweet'] = round(media['num_media'] / tweets_number, 3)
        symbols['symbols_per_tweet'] = round(symbols['num_symbols'] / tweets_number, 3)
       
        self.timeline['favorite_per_tweet'] = round(self.timeline['favorite_count'] / tweets_number, 3)
        self.timeline['retweet_per_tweet'] = round(self.timeline['retweet_count'] / tweets_number, 3)

        self.hashtags = hash_dict
        self.mentions = mentions
        self.urls = urls
        self.media=media
        self.symbols=symbols


    def __repr__(self):
        return str({
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'verified':self.verified,
            'followers':self.followers,
            'following':self.following,
            'listed':self.listed,
            'favorites':self.favorites,
            'location':self.location,
            'tweets_number':self.tweets_number,
            'last':self.last,
        })

    @staticmethod
    def from_repr(data):
        timeline = [Tweet.from_repr(t) for t in data['timeline']]
        return User(data['id'], data['name'],data['location'], data['description'],
            data['verified'],data['followers'],data['following'], data['listed'],
            data['favorites'], len(timeline),data['last'],timeline)

    def to_repr(self):
        return {
            'id':self.id,
            'name':self.name,
            'followers':self.followers,
            'following':self.following,
            'listed':self.listed,
            'description':self.description,
            'verified':self.verified,
            'favorites':self.favorites,
            'location':self.location,
            'tweets_number':self.tweets_number,
            'last':self.last,
            'timeline':[tweet.to_repr() for tweet in self.timeline]
        }

    '''
    def __repr__(self):
        return 'User(id = {id},' \
               ' name = {name},' \
                ' followers = {followers},' \
                ' following = {following},' \
                ' listed = {listed},' \
                ' favorites = {fav},' \
                ' verified = {ver}, ' \
                ' number of tweets = {tweets_num}\n' \
                ' hashtags = {hash}\n' \
                ' mentions = {ment}\n' \
                ' urls = {urls}\n' \
                ' media = {media}\n' \
                ' symbols = {sym}\n' \
                'sentiment = {sent})'.format(
                    id=self.id,
                    name=self.name,
                    fav=self.favorites,
                    followers = self.followers,
                    following = self.following,
                    listed = self.listed,
                    ver = self.verified,
                    sent = self.sentiment,
                    tweets_num = self.timeline['tweets_number'],
                    hash = self.hashtags,
                    ment = self.mentions,
                    urls = self.urls,
                    media = self.media,
                    sym = self.symbols
                )
    '''

    def to_json(self):
        toRtn = {
            'userID' : self.id,
            'followers' : self.followers,
            'following' : self.following,
            'listed' : self.listed,
            'user_favorite' : self.favorites,
            'verified' : self.verified,
            'sentiment':self.sentiment,
            'timeline':{
                'tweetsIDs' : [t.id for t in self.timeline['timeline']],
                'tweets_count' : self.timeline['tweets_number'],
                'favorite_count' : self.timeline['favorite_count'],
                'retweet_count' : self.timeline['retweet_count'],
                'favorite_per_tweet' : self.timeline['favorite_per_tweet'],
                'retweet_per_tweet' : self.timeline['retweet_per_tweet']
                #Possible TODO: max and min number of fav and ret
            },
            'entities':{
                'hashtags' : self.hashtags,
                'mentions' : self.mentions,
                'urls' : self.urls,
                'media' : self.media,
                'symbols' : self.symbols          
            }
        }

        #Write toRtn dict into a json file
        with open('UserJson/'+str(self.id)+".json", 'w') as f:
            json.dump(toRtn, f, indent=4)


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

    @staticmethod
    def from_repr(data):
        return Tweet(data['id'], data['text'], data['favourite_count'],data['hashtags'],
        data['media'], data['retweet_count'], data['urls'], datetime.strptime(data['created_at'], "%d/%m/%Y, %H:%M:%S"),
        data['mentions'], [], data['place'], data['tweet_type'])

    def __init__(self, id, text, favorite, hashtags, media, retweet_count, urls, created_at, mentions, symbols, place, tweet_type):
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
        #quote_count, reply_count
        #QUOTE_count and reply_count are not available with freeAPI
        #self.quote_count = quote_count
        self.urls = urls
        self.mentions = mentions
        self.created_at = created_at
        self.symbols = symbols
        self.place=place
        self.tweet_type=tweet_type

        #self.sentApi = SentimentAnalyzer()

        #Call the method for the computation of the sentiment values

        #self.__compute_sentiment()

        #self.sentiment=0

    def __repr__(self):
        return str(self.to_repr())

    def to_repr(self):
        return {'id':self.id,
            'created_at':self.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
            'text':self.text,
            'media':self.media,
            'hashtags':self.hashtags,
            'mentions':self.mentions,
            'urls':self.urls,
            'place':self.place,
            'favourite_count':self.favorite,
            'retweet_count':self.retweet_count,
            'tweet_type':self.tweet_type}
            
    def __compute_sentiment(self):
        #Send the request
        response = self.sentApi.text_request(self.text)
        '''
            Response has the following parameters:
                timestamp, time, lang, langConfidence, sentiment: {type, score}
        '''
        self.sentiment = response.get('sentiment')

        #Entities and Topics
        #Send request
        response = self.sentApi.entities_topics_request(self.text)

        self.semantic = response

    # Comparison based on the tweet ID. the greater it is, the older the tweet is
    def __eq__(self, t):
        return self.id == t.id

    def __lt__(self, t):
        return self.id < t.id

    def __gt__(self, t):
        return self.id > t.id

    def __hash__(self):
        return self.id
