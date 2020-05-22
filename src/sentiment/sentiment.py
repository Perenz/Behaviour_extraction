#To enrich tweet object with sentiment polarity

#Instal dandelionAPI
#See DOC https://python-dandelion-eu.readthedocs.io/en/latest/
#Python does not contain sentiment analysis API

#Use HTTP requests

import requests
import os, json



class SentimentAnalyzer:
    def __init__(self):
        KEYS = os.path.join(os.path.dirname(__file__), 'keys.json')
        keys = None
        with open(KEYS) as f:
            keys = json.load(f)

        self.token = keys['token']
        self.session = requests.Session()

    def text_request(self, text):
        '''
            Return the sentiment score and the type of the text
            Language (lang) is set at auto
        '''

        #Params for the request
        PARAMS = {'token': self.token, 'text': text}
        
        endpoint = "https://api.dandelion.eu/datatxt/sent/v1"
        toRtn = self.session.get(url= endpoint, params=PARAMS).json()
        #toRtn = {'error': True} #DEBUG
        
        #Handle error returning a neutral sentiment
        #Ex: Language not recognized
        if toRtn.get('error') == True:
            return {'sentiment':{'type':'neutral', 'score':0.0}}
        else:
            return toRtn


    def entities_topics_request(self, text):
        '''
            Return list of entities and list of topics
        '''
        #Parameters for the request
        #Social.hashtag and mention to parse these social network aspects
        #include categories to add category information from Wiki
        PARAMS = {'token': self.token, 'text':text, 'social.hashtag':True, 'social.mention':True, 'include':'categories'}

        #Have a look at request keep-alive TODO
        endpoint = "https://api.dandelion.eu/datatxt/nex/v1"
        toRtn = self.session.get(url=endpoint, params=PARAMS).json()

        if toRtn.get('error') == True:
            return {'entities':[], 'topics':[]}
        else:
            
            sem = []
            keys = ['title','confidence', 'categories']
            for a in toRtn.get('annotations'):        
                sem.append({key:a.get(key, []) for key in keys})

            return sem