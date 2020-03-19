#To enrich tweet object with sentiment polarity

#Instal dandelionAPI
#See DOC https://python-dandelion-eu.readthedocs.io/en/latest/
#Python does not contain sentiment analysis API

#Use HTTP requests

import requests
import os, json

endpoint = "https://api.dandelion.eu/datatxt/sent/v1"


class SentimentAnalyzer:
    def __init__(self):
        KEYS = os.path.join(os.path.dirname(__file__), 'keys.json')
        keys = None
        with open(KEYS) as f:
            keys = json.load(f)

        self.token = keys['token']

    def text_request(self, text):
        '''
            Return the sentiment score and the type of the text
            Language (lang) is set at auto
        '''

        #Params for the request
        PARAMS = {'token': self.token, 'text': text}
        
        toRtn = requests.get(url= endpoint, params=PARAMS).json()
        
        #Handle error returning a neutral sentiment
        #Ex: Language not recognized
        if toRtn.get('error') == True:
            return {'sentiment':{'type':'neutral', 'score':0.0}}
        else:
            return toRtn
        
